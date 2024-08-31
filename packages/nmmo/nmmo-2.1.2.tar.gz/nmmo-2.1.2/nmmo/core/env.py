import os
import functools
from typing import Any, Dict, List, Callable
from collections import defaultdict
from copy import deepcopy

import gymnasium as gym
import dill
import numpy as np
from pettingzoo.utils.env import AgentID, ParallelEnv

import nmmo
from nmmo.core import realm
from nmmo.core import game_api
from nmmo.core.config import Default
from nmmo.core.observation import Observation
from nmmo.core.tile import Tile
from nmmo.entity.entity import Entity
from nmmo.systems.item import Item
from nmmo.task.game_state import GameStateGenerator
from nmmo.lib import seeding

class Env(ParallelEnv):
  # Environment wrapper for Neural MMO using the Parallel PettingZoo API

  #pylint: disable=no-value-for-parameter
  def __init__(self,
               config: Default = nmmo.config.Default(),
               seed = None):
    '''Initializes the Neural MMO environment.

    Args:
      config (Default, optional): Configuration object for the environment.
      Defaults to nmmo.config.Default().
      seed (int, optional): Random seed for the environment. Defaults to None.
    '''
    self._np_random = None
    self._np_seed = None
    self._reset_required = True
    self.seed(seed)
    super().__init__()

    self.config = config
    self.config.env_initialized = True

    # Generate maps if they do not exist
    config.MAP_GENERATOR(config).generate_all_maps(self._np_seed)
    self.realm = realm.Realm(config, self._np_random)
    self.tile_map = None
    self.tile_obs_shape = None

    self.possible_agents = self.config.POSSIBLE_AGENTS
    self._alive_agents = None
    self._current_agents = None
    self._dead_this_tick = None
    self.scripted_agents = set()

    self.obs = {agent_id: Observation(self.config, agent_id)
                for agent_id in self.possible_agents}
    self._dummy_task_embedding = np.zeros(self.config.TASK_EMBED_DIM, dtype=np.float16)
    self._dummy_obs = Observation(self.config, 0).empty_obs
    self._comm_obs = {}

    self._gamestate_generator = GameStateGenerator(self.realm, self.config)
    self.game_state = None
    self.tasks = None
    self.agent_task_map = {}

    # curriculum file path, if provided, should exist
    self.curriculum_file_path = config.CURRICULUM_FILE_PATH
    if self.curriculum_file_path is not None:
      # try to open the file to check if it exists
      with open(self.curriculum_file_path, 'rb') as f:
        dill.load(f)
      f.close()

    self.game = None
    # NOTE: The default game runs with the full provided config and unmodded realm.reset()
    self.default_game = game_api.DefaultGame(self)
    self.game_packs: List[game_api.Game] = None
    if config.GAME_PACKS:  # assume List[Tuple(class, weight)]
      self.game_packs = [game_cls(self, weight) for game_cls, weight in config.GAME_PACKS]

  @functools.cached_property
  def _obs_space(self):
    def box(rows, cols):
      return gym.spaces.Box(
          low=-2**15, high=2**15-1,
          shape=(rows, cols),
          dtype=np.int16)
    def mask_box(length):
      return gym.spaces.Box(low=0, high=1, shape=(length,), dtype=np.int8)

    # NOTE: obs space-related config attributes must NOT be changed after init
    num_tile_attributes = len(Tile.State.attr_name_to_col)
    num_tile_attributes += 1 if self.config.original["PROVIDE_DEATH_FOG_OBS"] else 0
    obs_space = {
      "CurrentTick": gym.spaces.Discrete(self.config.MAX_HORIZON),
      "AgentId": gym.spaces.Discrete(self.config.PLAYER_N+1),
      "Tile": box(self.config.MAP_N_OBS, num_tile_attributes),
      "Entity": box(self.config.PLAYER_N_OBS, Entity.State.num_attributes),
      "Task": gym.spaces.Box(low=-2**15, high=2**15-1,
                             shape=(self.config.TASK_EMBED_DIM,),
                             dtype=np.float16),
    }

    # NOTE: cannot turn on a game system that was not enabled during env init
    if self.config.original["ITEM_SYSTEM_ENABLED"]:
      obs_space["Inventory"] = box(self.config.INVENTORY_N_OBS, Item.State.num_attributes)

    if self.config.original["EXCHANGE_SYSTEM_ENABLED"]:
      obs_space["Market"] = box(self.config.MARKET_N_OBS, Item.State.num_attributes)

    if self.config.original["COMMUNICATION_SYSTEM_ENABLED"]:
      # Comm obs cols: id, row, col, message
      obs_space["Communication"] = box(self.config.COMMUNICATION_N_OBS, 4)

    if self.config.original["PROVIDE_ACTION_TARGETS"]:
      mask_spec = deepcopy(self._atn_space)
      for atn_str in mask_spec:
        for arg_str in mask_spec[atn_str]:
          mask_spec[atn_str][arg_str] = mask_box(self._atn_space[atn_str][arg_str].n)
      obs_space["ActionTargets"] = mask_spec

    return gym.spaces.Dict(obs_space)

  # pylint: disable=method-cache-max-size-none
  @functools.lru_cache(maxsize=None)
  def observation_space(self, agent: AgentID):
    '''Neural MMO Observation Space

      Args:
        agent (AgentID): The ID of the agent.
        
      Returns:
        gym.spaces.Dict: The observation space for the agent.
    '''
    return self._obs_space

  # NOTE: make sure this runs once during trainer init and does NOT change afterwards
  @functools.cached_property
  def _atn_space(self):
    actions = {}
    for atn in sorted(nmmo.Action.edges(self.config)):
      if atn.enabled(self.config):
        actions[atn.__name__] = {}  # use the string key
        for arg in sorted(atn.edges):
          n = arg.N(self.config)
          actions[atn.__name__][arg.__name__] = gym.spaces.Discrete(n)
        actions[atn.__name__] = gym.spaces.Dict(actions[atn.__name__])
    return gym.spaces.Dict(actions)

  @functools.cached_property
  def _str_atn_map(self):
    '''Map action and argument names to their corresponding objects'''
    str_map = {}
    for atn in nmmo.Action.edges(self.config):
      str_map[atn.__name__] = atn
      for arg in atn.edges:
        str_map[arg.__name__] = arg
    return str_map

  # pylint: disable=method-cache-max-size-none
  @functools.lru_cache(maxsize=None)
  def action_space(self, agent: AgentID):
    '''Neural MMO Action Space

      Args:
        agent (AgentID): The ID of the agent.

      Returns:
        gym.spaces.Dict: The action space for the agent.
    '''
    return self._atn_space

  ############################################################################
  # Core API

  def reset(self, seed=None, options=None,  # PettingZoo API args
            map_id=None,
            make_task_fn: Callable=None,
            game: game_api.Game=None):
    '''Resets the environment and returns the initial observations.

      Args:
        seed (int, optional): Random seed for the environment. Defaults to None.
        options (dict, optional): Additional options for resetting the environment.
          Defaults to None.
        map_id (int, optional): The ID of the map to load. Defaults to None.
        make_task_fn (callable, optional): Function to create tasks. Defaults to None.
        game (Game, optional): The game to be played. Defaults to None.

      Returns:
        tuple: A tuple containing:
          - obs (dict): Dictionary mapping agent IDs to their initial observations.
          - info (dict): Dictionary containing additional information.
    '''
    # If options are provided, override the kwargs
    if options is not None:
      map_id = options.get('map_id', None) or map_id
      make_task_fn = options.get('make_task_fn', None) or make_task_fn
      game = options.get('game', None) or game

    self.seed(seed)
    map_dict = self._load_map_file(map_id)

    # Choose and reset the game, realm, and tasks
    if make_task_fn is not None:
      # Use the provided tasks with the default game (full config, unmodded realm)
      self.tasks = make_task_fn()
      self.game = self.default_game
      self.game.reset(self._np_random, map_dict, self.tasks)  # also does realm.reset()
    elif game is not None:
      # Use the provided game, which comes with its own tasks
      self.game = game
      self.game.reset(self._np_random, map_dict)
      self.tasks = self.game.tasks
    elif self.curriculum_file_path is not None or self.game_packs is not None:
      # Assume training -- pick a random game from the game packs
      self.game = self.default_game
      if self.game_packs:
        weights = [game.sampling_weight for game in self.game_packs]
        self.game = self._np_random.choice(self.game_packs, p=weights/np.sum(weights))
      self.game.reset(self._np_random, map_dict)
      # use the sampled tasks from self.game
      self.tasks = self.game.tasks
    else:
      # Just reset the same game and tasks as before
      self.game = self.default_game  # full config, unmodded realm
      self.game.reset(self._np_random, map_dict, self.tasks)  # use existing tasks
      if self.tasks is None:
        self.tasks = self.game.tasks
      else:
        for task in self.tasks:
          task.reset()

    # Reset the agent vars
    self._alive_agents = self.possible_agents
    self._dead_this_tick = {}
    self._map_task_to_agent()
    self._current_agents = self.possible_agents  # tracking alive + dead_this_tick

    # Check scripted agents
    self.scripted_agents.clear()
    for eid, ent in self.realm.players.items():
      if isinstance(ent.agent, nmmo.Scripted):
        self.scripted_agents.add(eid)
        ent.agent.set_rng(self._np_random)

    # Tile map placeholder, to reduce redudunt obs computation
    self.tile_map = Tile.Query.get_map(self.realm.datastore, self.config.MAP_SIZE)
    if self.config.PROVIDE_DEATH_FOG_OBS:
      fog_map = np.round(self.realm.fog_map)[:,:,np.newaxis].astype(np.int16)
      self.tile_map = np.concatenate((self.tile_map, fog_map), axis=-1)
    self.tile_obs_shape = (self.config.PLAYER_VISION_DIAMETER**2, self.tile_map.shape[-1])

    # Reset the obs, game state generator
    infos = {}
    for agent_id in self.possible_agents:
      # NOTE: the tasks for each agent is in self.agent_task_map, and task embeddings are
      #   available in each task instance, via task.embedding
      #   For now, each agent is assigned to a single task, so we just use the first task
      # TODO: can the embeddings of multiple tasks be superposed while preserving the
      #   task-specific information? This needs research
      task_embedding = self._dummy_task_embedding
      if agent_id in self.agent_task_map:
        task_embedding = self.agent_task_map[agent_id][0].embedding
        infos[agent_id] = {"task": self.agent_task_map[agent_id][0].name}
      self.obs[agent_id].reset(self.realm.map.habitable_tiles, task_embedding)
    self._compute_observations()
    self._gamestate_generator = GameStateGenerator(self.realm, self.config)
    if self.game_state is not None:
      self.game_state.clear_cache()
      self.game_state = None

    self._reset_required = False

    return {a: o.to_gym() for a,o in self.obs.items()}, infos

  def _load_map_file(self, map_id: int=None):
    '''Loads a map file, which is a 2D numpy array'''
    map_dict= {}
    map_id = map_id or self._np_random.integers(self.config.MAP_N) + 1
    map_file_path = os.path.join(self.config.PATH_CWD, self.config.PATH_MAPS,
                                 self.config.PATH_MAP_SUFFIX.format(map_id))
    map_dict["map"] = np.load(map_file_path)
    if self.config.MAP_RESET_FROM_FRACTAL:
      fractal_file_path = os.path.join(self.config.PATH_CWD, self.config.PATH_MAPS,
                                       self.config.PATH_FRACTAL_SUFFIX.format(map_id))
      map_dict["fractal"] = np.load(fractal_file_path).astype(float)
    return map_dict

  def _map_task_to_agent(self):
    self.agent_task_map.clear()
    for agent_id in self.agents:
      self.realm.players[agent_id].my_task = None
    for task in self.tasks:
      if task.embedding is None:
        task.set_embedding(self._dummy_task_embedding)
      # map task to agents
      for agent_id in task.assignee:
        if agent_id in self.agent_task_map:
          self.agent_task_map[agent_id].append(task)
        else:
          self.agent_task_map[agent_id] = [task]

    # for now we only support one task per agent
    if self.config.ALLOW_MULTI_TASKS_PER_AGENT is False:
      for agent_id, agent_tasks in self.agent_task_map.items():
        assert len(agent_tasks) == 1, "Only one task per agent is supported"
        self.realm.players[agent_id].my_task = agent_tasks[0]

  def step(self, actions: Dict[int, Dict[str, Dict[str, Any]]]):
    '''Performs one step in the environment given the provided actions.

      Args:
        actions (dict): Dictionary mapping agent IDs to their actions.

      Returns:
        tuple: A tuple containing:
          - obs (dict): Dictionary mapping agent IDs to their new observations.
          - rewards (dict): Dictionary mapping agent IDs to their rewards.
          - terminated (dict): Dictionary mapping agent IDs to whether they reached 
            a terminal state.
          - truncated (dict): Dictionary mapping agent IDs to whether the episode was
            truncated (e.g. reached maximum number of steps).
          - infos (dict): Dictionary containing additional information.
    '''
    assert not self._reset_required, 'step() called before reset'
    # Add in scripted agents' actions, if any
    if self.scripted_agents:
      actions = self._compute_scripted_agent_actions(actions)

    # Drop invalid actions of BOTH neural and scripted agents
    #   we don't need _deserialize_scripted_actions() anymore
    actions = self._validate_actions(actions)
    # Execute actions
    self._dead_this_tick, dead_npcs = self.realm.step(actions)
    self._alive_agents = list(self.realm.players.keys())
    self._current_agents = list(set(self._alive_agents + list(self._dead_this_tick.keys())))

    terminated = {}
    for agent_id in self._current_agents:
      if agent_id in self._dead_this_tick:
        # NOTE: Even though players can be resurrected, the time of death must be marked.
        terminated[agent_id] = True
      else:
        terminated[agent_id] = False

    if self.realm.tick >= self.config.HORIZON:
      self._alive_agents = []  # pettingzoo requires agents to be empty

    # Update the game stats, determine winners, etc.
    # Also, resurrect dead agents and/or spawn new npcs if the game allows it
    self.game.update(terminated, self._dead_this_tick, dead_npcs)

    # Some games do additional player cull during update(), so process truncated here
    truncated = {}
    for agent_id in self._current_agents:
      if self.realm.tick >= self.config.HORIZON:
        truncated[agent_id] = agent_id in self.realm.players
      else:
        truncated[agent_id] = False

    # Store the observations, since actions reference them
    self._compute_observations()
    gym_obs = {a: self.obs[a].to_gym() for a in self._current_agents}

    rewards, infos = self._compute_rewards()

    # NOTE: all obs, rewards, dones, infos have data for each agent in self.agents
    return gym_obs, rewards, terminated, truncated, infos

  @property
  def dead_this_tick(self):
    return self._dead_this_tick

  def _validate_actions(self, actions: Dict[int, Dict[str, Dict[str, Any]]]):
    '''Deserialize action arg values and validate actions
       For now, it does a basic validation (e.g., value is not none).
    '''
    validated_actions = {}

    for ent_id, atns in actions.items():
      if ent_id not in self.realm.players:
        #assert ent_id in self.realm.players, f'Entity {ent_id} not in realm'
        continue # Entity not in the realm -- invalid actions

      entity = self.realm.players[ent_id]
      if not entity.alive:
        #assert entity.alive, f'Entity {ent_id} is dead'
        continue # Entity is dead -- invalid actions

      validated_actions[ent_id] = {}

      for atn_key, args in sorted(atns.items()):
        action_valid = True
        deserialized_action = {}

        # If action/system is not enabled, it's not in self._str_atn_map
        if isinstance(atn_key, str) and atn_key not in self._str_atn_map:
          action_valid = False
          continue

        atn = self._str_atn_map[atn_key] if isinstance(atn_key, str) else atn_key
        if not atn.enabled(self.config):  # This can change from episode to episode
          action_valid = False
          continue

        for arg_key, val in sorted(args.items()):
          arg = self._str_atn_map[arg_key] if isinstance(arg_key, str) else arg_key
          obj = arg.deserialize(self.realm, entity, val, self.obs[ent_id])
          if obj is None:
            action_valid = False
            break
          deserialized_action[arg] = obj

        if action_valid:
          validated_actions[ent_id][atn] = deserialized_action

    return validated_actions

  def _compute_scripted_agent_actions(self, actions: Dict[int, Dict[str, Dict[str, Any]]]):
    '''Compute actions for scripted agents and add them into the action dict'''
    dead_agents = set()
    for agent_id in self.scripted_agents:
      if agent_id in self.realm.players:
        # override the provided scripted agents' actions
        actions[agent_id] = self.realm.players[agent_id].agent(self.obs[agent_id])
      else:
        dead_agents.add(agent_id)

    # remove the dead scripted agent from the list
    self.scripted_agents -= dead_agents

    return actions

  def _compute_observations(self):
    radius = self.config.PLAYER_VISION_RADIUS
    market = Item.Query.for_sale(self.realm.datastore) \
      if self.config.EXCHANGE_SYSTEM_ENABLED else None
    self._update_comm_obs()
    if self.config.PROVIDE_DEATH_FOG_OBS:
      self.tile_map[:, :, -1] = np.round(self.realm.fog_map)

    for agent_id in self._current_agents:
      if agent_id not in self.realm.players:
        self.obs[agent_id].set_agent_dead()
      else:
        r, c = self.realm.players.get(agent_id).pos
        visible_entities = Entity.Query.window(self.realm.datastore, r, c, radius)
        visible_tiles = self.tile_map[r-radius:r+radius+1,
                                      c-radius:c+radius+1, :].reshape(self.tile_obs_shape)
        inventory = Item.Query.owned_by(self.realm.datastore, agent_id) \
          if self.config.ITEM_SYSTEM_ENABLED else None
        comm_obs = self._comm_obs[agent_id] \
          if self.config.COMMUNICATION_SYSTEM_ENABLED else None
        self.obs[agent_id].update(self.realm.tick, visible_tiles, visible_entities,
                                  inventory=inventory, market=market, comm=comm_obs)

  def _update_comm_obs(self):
    if not self.config.COMMUNICATION_SYSTEM_ENABLED:
      return
    comm_obs = Entity.Query.comm_obs(self.realm.datastore)
    agent_ids = comm_obs[:, Entity.State.attr_name_to_col['id']]
    self._comm_obs.clear()
    for agent_id in self.realm.players:
      if agent_id not in self._comm_obs:
        my_team = [agent_id] if agent_id not in self.agent_task_map \
          else self.agent_task_map[agent_id][0].assignee  # NOTE: first task only
        team_obs = [comm_obs[agent_ids == eid] for eid in my_team]
        if len(team_obs) == 1:
          team_obs = team_obs[0]
        else:
          team_obs = np.concatenate(team_obs, axis=0)
        for eid in my_team:
          self._comm_obs[eid] = team_obs

  def _compute_rewards(self):
    # Initialization
    agents = set(self._current_agents)
    infos = {agent_id: {'task': {}} for agent_id in agents}
    rewards = defaultdict(int)

    # Clean up unnecessary game state, which cause memory leaks
    if self.game_state is not None:
      self.game_state.clear_cache()
      self.game_state = None

    # Compute Rewards and infos
    self.game_state = self._gamestate_generator.generate(self.realm, self.obs)
    for task in self.tasks:
      if agents.intersection(task.assignee): # evaluate only if the agents are current
        task_rewards, task_infos = task.compute_rewards(self.game_state)
        for agent_id, reward in task_rewards.items():
          if agent_id in agents:
            rewards[agent_id] = rewards.get(agent_id,0) + reward
            infos[agent_id]['task'][task.name] = task_infos[agent_id] # include progress, etc.
      else:
        task.close()  # To prevent memory leak

    # Reward for frozen agents (recon, resurrected, frozen) is 0 because they cannot act
    for agent_id, agent in self.realm.players.items():
      if agent.status.frozen:
        rewards[agent_id] = 0

    # Reward for dead agents is defined by the game
    # NOTE: Resurrected agents are frozen and in the realm.players, so run through
    # self._dead_this_tick to give out the dead reward
    if self.game.assign_dead_reward:
      for agent_id in self._dead_this_tick:
        rewards[agent_id] = -1

    return rewards, infos

  ############################################################################
  # PettingZoo API
  ############################################################################

  def render(self, mode='human'):
    '''For conformity with the PettingZoo API only; rendering is external'''

  @property
  def agents(self) -> List[AgentID]:
    '''For conformity with the PettingZoo API; retuning only the alive agents'''
    return self._alive_agents

  def close(self):
    '''For conformity with the PettingZoo API only; rendering is external'''

  def seed(self, seed=None):
    '''Reseeds the environment. reset() must be called after seed(), and before step().
       - self._np_seed is None: seed() has not been called, e.g. __init__() -> new RNG
       - self._np_seed is set, and seed is not None: seed() or reset() with seed -> new RNG

       If self._np_seed is set, but seed is None
         probably called from reset() without seed, so don't change the RNG
    '''
    if self._np_seed is None or seed is not None:
      self._np_random, self._np_seed = seeding.np_random(seed)
      self._reset_required = True

  def state(self) -> np.ndarray:
    raise NotImplementedError

  metadata = {'render.modes': ['human'], 'name': 'neural-mmo'}
