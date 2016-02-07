from .action_base import *
from . import placeholders
from .util import *

class VirtualAction(ActionBase):
  """An action that wraps and modifies another action."""

  def __init__(self, action):
    super().__init__()
    self.action = action

  def __str__(self):
    return "%s(%s)" % (self.__class__.__name__, self.action)

  @property
  def player(self):
    return self.action.player

  @player.setter
  def player(self, player):
    self.action = self.action.with_player(player)

  def concrete_action(self):
    return self.action.concrete_action()

class FactionAction(VirtualAction):
  """An action taken by a player on behalf of their faction."""

  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction

class Compelled(VirtualAction):
  """An action that MUST be used each night."""

  compelled = True

  def matches(self, other, **kwargs):
    return self.action.matches(other, **kwargs)

  def random_instance(self, **kwargs):
    return self.action.random_instance(**kwargs)
