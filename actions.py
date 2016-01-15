from .events import *
from .log import *

class Action(object):
  def __init__(self, targets):
    if not isinstance(targets, list):
      targets = [targets]
    self.targets = targets

class Kill(Action):
  precedence = 1000

  def resolve(self, player, state):
    for target in self.targets:
      if target not in state.protected:
        target.alive = False
        state.log(Died(target))

class Investigate(Action):
  precedence = 100

  def __init__(self, targets):
    super().__init__(targets)

  def resolve(self, player, state):
    for target in self.targets:
      state.log(TurntUp(target, target.alignment, to=player))

class Protect(Action):
  precedence = 100

  def resolve(self, player, state):
    for target in self.targets:
      state.protected.add(target)
