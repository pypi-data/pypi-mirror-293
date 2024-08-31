from __future__ import annotations
from typing import Dict, Union, Iterable, TYPE_CHECKING
from collections import OrderedDict
from collections.abc import Set, Sequence
import weakref

if TYPE_CHECKING:
  from nmmo.task.game_state import GameState, GroupView

class Group(Sequence, Set):
  ''' An immutable, ordered, unique group of agents involved in a task
  '''
  def __init__(self,
               agents: Union(Iterable[int], int),
               name: str=None):

    if isinstance(agents, int):
      agents = (agents,)
    assert len(agents) > 0, "Team must have at least one agent"
    self.name = name if name else f"Agent({','.join([str(e) for e in agents])})"
    # Remove duplicates
    self._agents = tuple(OrderedDict.fromkeys(sorted(agents)).keys())
    if not isinstance(self._agents,tuple):
      self._agents = (self._agents,)

    self._sd: GroupView = None
    self._gs: GameState = None

    self._hash = hash(self._agents)

  @property
  def agents(self):
    return self._agents

  def union(self, o: Group):
    return Group(self._agents + o.agents)

  def intersection(self, o: Group):
    return Group(set(self._agents).intersection(set(o.agents)))

  def __eq__(self, o):
    return self._agents == o

  def __len__(self):
    return len(self._agents)

  def __hash__(self):
    return self._hash

  def __getitem__(self, key):
    if len(self) == 1 and key == 0:
      return self
    return Group((self._agents[key],), f"{self.name}.{key}")

  def __contains__(self, key):
    if isinstance(key, int):
      return key in self.agents
    return Sequence.__contains__(self, key)

  def __str__(self) -> str:
    return str(self._agents)

  def __int__(self) -> int:
    assert len(self._agents) == 1, "Group is not a singleton"
    return int(self._agents[0])

  def __copy__(self):
    return self
  def __deepcopy__(self, memo):
    return Group(self.agents, self.name)

  def description(self) -> Dict:
    return {
      "type": "Group",
      "name": self.name,
      "agents": self._agents
    }

  def clear_prev_state(self) -> None:
    if self._gs is not None:
      self._gs.clear_cache()  # prevent memory leak
      self._gs = None
    if self._sd is not None:
      weakref.ref(self._sd)  # prevent memory leak
      self._sd = None

  def update(self, gs: GameState) -> None:
    self.clear_prev_state()
    self._gs = gs
    self._sd = gs.get_subject_view(self)

  def __getattr__(self, attr):
    return self._sd.__getattribute__(attr)

def union(*groups: Group) -> Group:
  """ Performs a big union over groups
  """
  agents = []
  for group in groups:
    for agent in group.agents:
      agents.append(agent)
  return Group(agents)

def complement(group: Group, universe: Group) -> Group:
  """ Returns the complement of group in universe
  """
  agents = []
  for agent in universe.agents:
    if not agent in group:
      agents.append(agent)
  return Group(agents)
