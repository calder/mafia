from .actions import *

class VirtualAction(object):
  def __init__(self, action):
    super().__init__()
    self.action = action

  def __str__(self):
    return "%s(%s)" % (self.__class__.__name__, self.action)

  @property
  def player(self):
    return self.action.player

  def select_action(self, actions):
    for action in reversed(actions):
      if self.matches(action):
        return action, action.action
    return None, None

  def matches(self, other):
    return all_fields_match(self, other)

class NoAction(VirtualAction):
  def __init__(self):
    super().__init__(None)

  def __str__(self):
    return "NoAction"

  def with_player(self, player):
    return self

  def matches(self, other):
    return False

class FactionAction(VirtualAction):
  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction
