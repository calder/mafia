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

  def select_action(self, game, player, actions):
    for action in reversed(actions):
      print(self.matches(action, game=game, player=player), self, action)
      if self.matches(action, game=game, player=player):
        return action, action.action
    return self._default_action(game, player)

  def _default_action(self, game, player):
    return None, None

  def matches(self, other, **kwargs):
    print("VirtualAction.matches", kwargs)
    return all_fields_match(self, other, **kwargs)

class FactionAction(VirtualAction):
  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction

class MandatoryAction(VirtualAction):
  def _default_action(self, game, player):
    return self.action.random_instance(game, player)

class NoAction(VirtualAction):
  def __init__(self):
    super().__init__(None)

  def __str__(self):
    return "NoAction"

  def with_player(self, player):
    return self

  def matches(self, other, **kwargs):
    return False
