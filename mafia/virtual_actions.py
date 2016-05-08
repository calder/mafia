import re

from .action_base import *
from . import placeholders
from .util import *

class VirtualAction(ActionBase):
  """An action that wraps and modifies another action."""

  def __init__(self, action):
    super().__init__()
    self.action = action

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

  def __str__(self):
    return "FactionAction(%s, %s)" % (self.faction, self.action)

  def parse(self, s, *, game, player):
    if player.faction.leader != player:
      raise InvalidAction("You are not the leader of your faction.")
    match = re.match(r"(\w+): (.*)", s)
    if not match:
      raise InvalidAction("Cannot parse faction action.")
    minion = game.player_named(match.group(1))
    if not minion:
      raise InvalidAction("%s is not yours to command." % match.group(1))
    return FactionAction(player.faction, self.action.parse(match.group(2), game=game, player=minion))

class OneOfAction(VirtualAction):
  """An action that may be one of a number of different actions."""
  def __init__(self, actions):
    self.actions = actions

  def __str__(self):
    actions = ", ".join([str(a) for a in self.actions])
    return "OneOfAction(%s)" % actions

  def matches(self, other, **kwargs):
    return any([a.matches(other, **kwargs) for a in self.actions])

  def parse(self, s, **kwargs):
    errors = []
    for action in self.actions:
      try:
        return action.parse(s, **kwargs)
      except (InvalidAction, e):
        errors.append(e)

    errors_str = "\n  - ".join([str(e) for e in errors])
    raise InvalidAction("Action doesn't match any available options:\n%s" % errors_str)

  def random_instance(self, *, game, **kwargs):
    return game.random.choice(self.actions).random_instance(game=game, **kwargs)

class Compelled(VirtualAction):
  """An action that MUST be used each night."""

  compelled = True

  def __str__(self):
    return "Compelled(%s)" % self.action

  def matches(self, other, **kwargs):
    return self.action.matches(other, **kwargs)

  def random_instance(self, **kwargs):
    return self.action.random_instance(**kwargs)
