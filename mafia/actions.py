from .events import *
from .log import *

class Action(object):
  def __init__(self, targets, *,
               blockable=True,
               doctorable=False,
               visible=True):
    if not isinstance(targets, list):
      targets = [targets]

    self.targets    = targets
    self.blockable  = blockable
    self.doctorable = doctorable
    self.visible    = visible

  def resolve(self, player, state):
    if self.blockable:
      if player in state.blocked:
        state.log(Blocked(player))
        return
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
    for target in self.targets:
      target.alive = False
      state.log(Died(target))

class Protect(Action):
  precedence = 100

  def _resolve(self, player, state):
    for target in self.targets:
      state.protected.add(target)

class Investigate(Action):
  precedence = 100

  def _resolve(self, player, state):
    for target in self.targets:
      state.log(TurntUp(target, target.alignment, to=player))

class Watch(Action):
  precedence = 2000

  def resolve_meta(self, player, state):
    visits = state.game.log.phase(state.night).type(Visited)
    for visit in visits:
      if visit.target in self.targets and visit.player is not player:
        state.log(SawVisit(visit.player, to=player))

class Roleblock(Action):
  precedence = 0

  def _resolve(self, player, state):
    for target in self.targets:
      state.blocked.add(target)
