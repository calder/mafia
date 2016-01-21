from .actions import *
from .placeholders import *
from .util import *

class VirtualAction(object):
  """An action that wraps and modifies another action."""

  compelled = False

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

  def with_player(self, player):
    clone = copy.copy(self)
    clone.player = player
    return clone

  def concrete_action(self):
    return self.action.concrete_action()

  def matches(self, other, **kwargs):
    return matches(self, other, **kwargs)

  def random_instance(self, **kwargs):
    clone = copy.copy(self)
    fill_randomly(clone, **kwargs)
    return clone

class FactionAction(VirtualAction):
  """An action taken by a player on behalf of their faction."""

  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction

class Compelled(VirtualAction):
  """An action that MUST be used each night."""

  compelled = True

  def matches(self, other, **kwargs):
    print("FactionAction.matches", self.action.matches(other, **kwargs), self, other)
    return self.action.matches(other, **kwargs)

  def random_instance(self, **kwargs):
    return self.action.random_instance(**kwargs)
