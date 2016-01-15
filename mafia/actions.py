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
    if self.visible:
      for target in self.targets:
        state.log(Targetted(player, target))
    if self.doctorable:
      for target in self.targets:
        if target in state.protected:
          state.log(Saved(target))
          return
    self._resolve(player, state)

class Kill(Action):
  precedence = 1000

  def __init__(self, targets, *, doctorable=True, **kwargs):
    super().__init__(targets, doctorable=doctorable, **kwargs)

  def _resolve(self, player, state):
    for target in self.targets:
      target.alive = False
      state.log(Died(target))

class Investigate(Action):
  precedence = 100

  def _resolve(self, player, state):
    for target in self.targets:
      state.log(TurntUp(target, target.alignment, to=player))

class Protect(Action):
  precedence = 100

  def _resolve(self, player, state):
    for target in self.targets:
      state.protected.add(target)
