from .events import *
from .log import *

class Action(object):
  def __init__(self, targets, *,
               blockable=True,
               doctorable=False,
               visible=True):
    if not isinstance(targets, list):
      targets = [targets]

    self.raw_targets = targets
    self.targets     = targets
    self.blockable   = blockable
    self.doctorable  = doctorable
    self.visible     = visible

  @property
  def target(self):
    return self.targets[0]

  @target.setter
  def set_target(self, target):
    self.targets[0] = target

  def resolve(self, player, state):
    if self.blockable:
      if player in state.blocked:
        state.log(Blocked(player))
        return
    self.targets = [state.target_map[t] for t in self.targets]
    for target in self.targets:
      state.log(Visited(player, target, visible=self.visible))
    if self.doctorable:
      for target in self.targets:
        if target in state.protected:
          state.log(Saved(target))
          return
    self._resolve(player, state)

  def _resolve(self, player, state):
    pass

  def resolve_meta(self, player, state):
    pass

class Kill(Action):
  precedence = 1000

  def __init__(self, targets, *, doctorable=True, **kwargs):
    super().__init__(targets, doctorable=doctorable, **kwargs)

  def _resolve(self, player, state):
    self.target.alive = False
    state.log(Died(self.target))

class Protect(Action):
  precedence = 200

  def _resolve(self, player, state):
    for target in self.targets:
      state.protected.add(target)

class Investigate(Action):
  precedence = 200

  def _resolve(self, player, state):
    for target in self.targets:
      state.log(TurntUp(target, target.alignment, to=player))

def send_targets(visits, *, to, log):
  targets = set(v.target for v in visits)
  for target in sorted(targets):
    log(SawVisit(target, to=to))

class Track(Action):
  precedence = 2000

  def resolve_meta(self, player, state):
    visits = state.game.log.phase(state.night).visits_by(self.target)
    send_targets(visits, to=player, log=state.log)

def send_visitors(visits, *, to, log):
  visitors = set(v.player for v in visits if v.player is not to)
  for visitor in sorted(visitors):
    log(SawVisitor(visitor, to=to))

class Watch(Action):
  precedence = 2000

  def resolve_meta(self, player, state):
    visits = state.game.log.phase(state.night).visits_to(self.target)
    send_visitors(visits, to=player, log=state.log)

class Autopsy(Action):
  precedence = 200

  def _resolve(self, player, state):
    visits = state.game.log.visits_to(self.target)
    send_visitors(visits, to=player, log=state.log)

class Roleblock(Action):
  precedence = 100

  def _resolve(self, player, state):
    for target in self.targets:
      state.blocked.add(target)

class Busdrive(Action):
  precedence = 0

  def __init__(self, player1, player2):
    super().__init__([player1, player2])

  def _resolve(self, player, state):
    a = self.targets[0]
    b = self.targets[1]
    state.target_map[a], state.target_map[b] = state.target_map[b], state.target_map[a]
