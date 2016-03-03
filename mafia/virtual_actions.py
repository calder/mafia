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

class OneOfAction(VirtualAction):
  """An action that may be one of a number of different actions."""
  def __init__(self, actions):
    self.actions = actions

  def matches(self, other, **kwargs):
    return any([a.matches(other, **kwargs) for a in self.actions])

  def random_instance(self, *, game, **kwargs):
    return game.random.choice(self.actions).random_instance(game=game, **kwargs)

class Compelled(VirtualAction):
  """An action that MUST be used each night."""

  compelled = True

  def matches(self, other, **kwargs):
    return self.action.matches(other, **kwargs)

  def random_instance(self, **kwargs):
    return self.action.random_instance(**kwargs)
