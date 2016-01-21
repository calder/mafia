from .events import *
from .log import *
from .placeholders import *
from .util import *

import copy

class TargetList(list):
  def matches(self, other, **kwargs):
    return len(self) == len(other) and \
           all([s.matches(o, **kwargs) for s, o in zip(self, other)])

  def random_instance(self, **kwargs):
    return TargetList([t.random_instance(**kwargs) for t in self])

class Action(object):
  compelled  = False  # Action must be taken
  doctorable = False  # Action can be protected against by a doctor

  def __init__(self, player, targets, **kwargs):
    if not isinstance(targets, list):
      targets = TargetList([targets])

    self.player      = player
    self.raw_targets = TargetList(targets)
    self.targets     = TargetList(targets)

  def __str__(self):
    targets = ", ".join([str(target) for target in self.targets])
    return "%s(%s, %s)" %(self.__class__.__name__, self.player, targets)

  @property
  def target(self):
    return self.targets[0]

  @target.setter
  def set_target(self, target):
    self.targets[0] = target

  def blocked(self, state):
    return self.player in state.blocked and self.player.role.blockable

  def resolve(self, state):
    # Apply roleblocking
    if self.blocked(state):
      state.log(Blocked(self.player))
      return

    # Apply busdriving
    self.targets = TargetList([state.target_map[t] for t in self.targets])

    # Record visit
    for target, raw_target in zip(self.targets, self.raw_targets):
      state.log(Visited(self.player, target, visible=self.player.role.visible,
                        original_target=raw_target))

    # Apply protection
    if self.doctorable and self.player.role.doctorable:
      if self.target in state.protected:
        state.log(Saved(target))
        return

    # Resolve action
    self._resolve(state)

  def resolve_post(self, state):
    if self.blocked(state): return
    self._resolve_post(state)

  def _resolve(self, state):
    pass

  def _resolve_post(self, state):
    pass

  def concrete_action(self):
    return self

  def with_player(self, player):
    clone = copy.copy(self)
    clone.player = player
    return clone

  def matches(self, other, **kwargs):
    return matches(self, other, **kwargs)

  def random_instance(self, **kwargs):
    clone = copy.copy(self)
    fill_randomly(clone, **kwargs)
    return clone

class Kill(Action):
  precedence = 1000
  doctorable = True

  def _resolve(self, state):
    self.target.alive = False
    state.log(Died(self.target))

class Protect(Action):
  precedence = 200

  def _resolve(self, state):
    for target in self.targets:
      state.protected.add(target)

class Investigate(Action):
  precedence = 200

  def _resolve(self, state):
    for target in self.targets:
      state.log(TurntUp(target.role.alignment, to=self.player))

def send_targets(visits, *, to, log):
  targets = set(v.target for v in visits)
  for target in sorted(targets):
    log(SawVisit(target, to=to))

class Track(Action):
  precedence = 2000

  def _resolve_post(self, state):
    visits = state.game.log.phase(state.night).visits_by(self.target)
    send_targets(visits, to=self.player, log=state.log)

def send_visitors(visits, *, to, log):
  visitors = set(v.player for v in visits if v.player is not to)
  for visitor in sorted(visitors):
    log(SawVisitor(visitor, to=to))

class Watch(Action):
  precedence = 2000

  def _resolve_post(self, state):
    visits = state.game.log.phase(state.night).visits_to(self.target)
    send_visitors(visits, to=self.player, log=state.log)

class Autopsy(Action):
  precedence = 200

  def _resolve(self, state):
    visits = state.game.log.visits_to(self.target)
    send_visitors(visits, to=self.player, log=state.log)

class Roleblock(Action):
  precedence = 100

  def _resolve(self, state):
    for target in self.targets:
      state.blocked.add(target)

class Busdrive(Action):
  precedence = 0

  def __init__(self, player, target1, target2):
    super().__init__(player, [target1, target2])

  def _resolve(self, state):
    a = self.targets[0]
    b = self.targets[1]
    state.target_map[a], state.target_map[b] = state.target_map[b], state.target_map[a]
