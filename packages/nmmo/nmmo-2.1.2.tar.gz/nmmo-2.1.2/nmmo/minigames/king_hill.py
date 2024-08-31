# pylint: disable=invalid-name, duplicate-code, unused-argument
import time
from nmmo.core.game_api import TeamBattle
from nmmo.task import task_spec, base_predicates
from nmmo.lib import utils, team_helper


def seize_task(dur_to_win):
  return task_spec.TaskSpec(
    eval_fn=base_predicates.SeizeCenter,
    eval_fn_kwargs={"num_ticks": dur_to_win},
    reward_to="team")

class KingoftheHill(TeamBattle):
  required_systems = ["TERRAIN", "COMBAT", "RESOURCE", "COMMUNICATION"]

  def __init__(self, env, sampling_weight=None):
    super().__init__(env, sampling_weight)

    self._seize_duration = 10  # determines the difficulty
    self.dur_step_size = 10
    self.max_seize_duration = 200
    self.adaptive_difficulty = True
    self.num_game_won = 2  # at the same duration, threshold to increase the difficulty
    self.map_size = 40
    self.score_scaler = .5

    # NOTE: This is a hacky way to get a hash embedding for a function
    # TODO: Can we get more meaningful embedding? coding LLMs are good but huge
    self.task_embedding = utils.get_hash_embedding(seize_task,
                                                   self.config.TASK_EMBED_DIM)

  @property
  def seize_duration(self):
    return self._seize_duration

  def set_seize_duration(self, seize_duration):
    self._seize_duration = seize_duration

  def is_compatible(self):
    return self.config.are_systems_enabled(self.required_systems)

  def reset(self, np_random, map_dict, tasks=None):
    super().reset(np_random, map_dict)
    self.history[-1]["map_size"] = self.map_size
    self.history[-1]["seize_duration"] = self.seize_duration

  def _set_config(self):
    self.config.reset()
    self.config.toggle_systems(self.required_systems)
    self.config.set_for_episode("MAP_CENTER", self.map_size)
    self.config.set_for_episode("ALLOW_MOVE_INTO_OCCUPIED_TILE", False)

    # Regenerate the map from fractal to have less obstacles
    self.config.set_for_episode("MAP_RESET_FROM_FRACTAL", True)
    self.config.set_for_episode("TERRAIN_WATER", 0.05)
    self.config.set_for_episode("TERRAIN_FOILAGE", 0.95)  # prop of stone tiles: 0.05
    self.config.set_for_episode("TERRAIN_SCATTER_EXTRA_RESOURCES", True)

    # Activate death fog
    self.config.set_for_episode("DEATH_FOG_ONSET", 32)
    self.config.set_for_episode("DEATH_FOG_SPEED", 1/16)
    self.config.set_for_episode("DEATH_FOG_FINAL_SIZE", 5)

    self._determine_difficulty()  # sets the seize duration

  def _determine_difficulty(self):
    # Determine the difficulty (the seize duration) based on the previous results
    if self.adaptive_difficulty and self.history \
       and self.history[-1]["result"]:  # the last game was won
      last_results = [r["result"] for r in self.history
                      if r["seize_duration"] == self.seize_duration]
      if sum(last_results) >= self.num_game_won:
        self._seize_duration = min(self.seize_duration + self.dur_step_size,
                                   self.max_seize_duration)

  def _set_realm(self, map_dict):
    self.realm.reset(self._np_random, map_dict, custom_spawn=True, seize_targets=["center"])
    # team spawn requires custom spawning
    team_loader = team_helper.TeamLoader(self.config, self._np_random)
    self.realm.players.spawn(team_loader)

  def _define_tasks(self):
    spec_list = [seize_task(self.seize_duration)] * len(self.teams)
    return task_spec.make_task_from_spec(self.teams, spec_list)

  @property
  def winning_score(self):
    if self._winners:
      time_limit = self.config.HORIZON
      speed_bonus = (time_limit - self.realm.tick) / time_limit
      alive_bonus = sum(1.0 for agent_id in self._winners if agent_id in self.realm.players)\
                    / len(self._winners)
      return (speed_bonus + alive_bonus) / 2  # set max to 1.0
    # No one succeeded
    return 0.0

  def _check_winners(self, terminated):
    assert self.config.TEAMS is not None, "Team battle mode requires TEAMS to be defined"
    winners = self._who_completed_task()
    if winners is not None:
      return winners

    if len(self.realm.seize_status) == 0:
      return None

    seize_results = list(self.realm.seize_status.values())

    # Time's up, and a team has seized the center
    if self.realm.tick == self.config.HORIZON:
      winners = []
      # Declare the latest seizing agent as the winner
      for agent_id, _ in seize_results:
        for task in self.tasks:
          if agent_id in task.assignee:
            winners += task.assignee
      return winners or None

    # Only one team remains and they have seized the center
    current_teams = self._check_remaining_teams()
    if len(current_teams) == 1:
      winning_team = list(current_teams.keys())[0]
      team_members = self.config.TEAMS[winning_team]
      for agent_id, _ in seize_results:
        # Check if the agent is in the winning team
        if agent_id in team_members:
          return team_members

    # No team has seized the center
    return None

  @staticmethod
  def test(env, horizon=30, seed=0):
    game = KingoftheHill(env)
    env.reset(game=game, seed=seed)

    # Check configs
    config = env.config
    assert config.are_systems_enabled(game.required_systems)
    assert config.TERRAIN_SYSTEM_ENABLED is True
    assert config.RESOURCE_SYSTEM_ENABLED is True
    assert config.COMBAT_SYSTEM_ENABLED is True
    assert config.ALLOW_MOVE_INTO_OCCUPIED_TILE is False
    assert config.DEATH_FOG_ONSET == 32
    assert env.realm.map.seize_targets == [(config.MAP_SIZE//2, config.MAP_SIZE//2)]

    start_time = time.time()
    for _ in range(horizon):
      env.step({})
    print(f"Time taken: {time.time() - start_time:.3f} s")  # pylint: disable=bad-builtin

    # Test if the difficulty increases
    org_seize_dur = game.seize_duration
    for result in [False]*7 + [True]*game.num_game_won:
      game.history.append({"result": result, "seize_duration": game.seize_duration})
      game._determine_difficulty()  # pylint: disable=protected-access
    assert game.seize_duration == (org_seize_dur + game.dur_step_size)

if __name__ == "__main__":
  import nmmo
  test_config = nmmo.config.Default()  # Medium, AllGameSystems
  test_config.set("TEAMS", team_helper.make_teams(test_config, num_teams=7))
  test_env = nmmo.Env(test_config)
  KingoftheHill.test(test_env)  # 0.59 s

  # performance test
  from tests.testhelpers import profile_env_step
  teams = test_config.TEAMS
  test_tasks = task_spec.make_task_from_spec(teams, [seize_task(30)]*len(teams))
  profile_env_step(tasks=test_tasks)
  # env._compute_rewards(): 0.24291237899888074
