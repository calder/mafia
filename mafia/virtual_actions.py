from .actions import *
from .placeholders import *

class VirtualAction(object):
  def __init__(self, action):
    super().__init__()
    self.action = action

  def __str__(self):
    return "%s(%s)" % (self.__class__.__name__, self.action)

  @property
  def player(self):
    return self.action.player

  def real_action(self):
    return self.action

  def select_action(self, actions, **kwargs):
    for action in reversed(actions):
      if self.matches(action, **kwargs):
        return action, action.real_action()
    return self._default_action(**kwargs)

  def _default_action(self, **kwargs):
    return None, None

  def matches(self, other, **kwargs):
    return all_fields_match(self, other, **kwargs)

class FactionAction(VirtualAction):
  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction

class Compelled(VirtualAction):
  def _default_action(self, **kwargs):
    return None, self.action.random_instance(**kwargs)

  def matches(self, other, **kwargs):
    return self.action.matches(other, **kwargs)

class NoAction(VirtualAction):
  def __init__(self):
    super().__init__(None)

  def __str__(self):
    return "NoAction"

  def with_player(self, player):
    return self

  def matches(self, other, **kwargs):
    return False
