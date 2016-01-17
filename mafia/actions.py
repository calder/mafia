from .events import *
from .log import *

class Action(object):
  blockable  = True   # Action can be roleblocked
  doctorable = False  # Action can be protected against by a doctor

  def __init__(self, player, targets):
    if not isinstance(targets, list):
      targets = [targets]

    self.player      = player
    self.raw_targets = targets
    self.targets     = targets

  @property
  def target(self):
    return self.targets[0]

  @target.setter
  def set_target(self, target):
    self.targets[0] = target

  def blocked(self, state):
    return self.player in state.blocked and self.blockable and self.player.role.blockable

  def resolve(self, state):
    # Apply roleblocking
    if self.blocked(state):
      state.log(Blocked(self.player))
      return

    # Apply busdriving
    self.targets = [state.target_map[t] for t in self.targets]

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
      state.log(TurntUp(target, target.role.alignment, to=self.player))

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
