from .log import *
from .phase import *
from .util import *
from .virtual_actions import *

class Night(Phase):
  """
  A single night in a Mafia game.

  Usage:
    night0 = Night(0)
    night0.add_action(Investigate(cop, goon))
    night0.add_action(FactionAction(mafia, Kill(cop, goon)))
    game.resolve(night0)
  """

  def __init__(self, number):
    self.number      = number
    self.raw_actions = []

  def __eq__(self, other):
    return isinstance(other, Night) and other.number == self.number

  def __str__(self):
    return "Night %d" % self.number

  def add_action(self, action):
    self.raw_actions.append(action)

  def _resolve(self, game):
    # Compile valid action set
    options = []
    for player in game.players:
      if player.action:
        for i in range(player.action_count):
          options.append(player.action)
    for faction in game.factions:
      if faction.action: options.append(faction.action)

    # Check actions
    actions = []
    for action in reversed(self.raw_actions):
      for option in options:
        if option.matches(action, game=game):
          actions.append(action.concrete_action())
          options.remove(option)
          break
    actions.reverse()

    # Add compelled actions
    for option in options:
      if option.compelled:
        instance = option.random_instance(game=game)
        actions.append(instance)

    # Add delayed actions
    actions = game.delayed_actions + actions
    game.delayed_actions = []

    # Resolve actions
    self.resolve_actions(actions, game=game)

    # Advance effects
    for player in game.all_players:
      for effect in player.effects:
        effect.expiration.advance_night()
