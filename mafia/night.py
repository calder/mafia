from .log import *
from .util import *
from .virtual_actions import *

import copy

class NightState(object):
  """The state of a night as its being resolved. Used to resolve Actions."""

  def __init__(self, night, game):
    self.night = night
    self.game = game
    self.target_map = identitydefaultdict()
    self.protected = set()
    self.blocked = set()

  def log(self, event):
    event.phase = self.night
    self.game.log.append(event)

class Night(object):
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

  def __str__(self):
    return "Night %d" % self.number

  def add_action(self, action):
    self.raw_actions.append(action)

  def resolve(self, game):
    state = NightState(self, game)

    # Compile valid action set
    options = set()
    for player in game.players:
      if player.role.action:
        options.add(player.role.action.with_player(player))
    del player  # Avoid confusion if used
    for faction in game.factions:
      if faction.action:
        options.add(FactionAction(faction, faction.action))

    # Check actions
    actions = []
    for action in reversed(self.raw_actions):
      for option in options:
        if option.matches(action, game=game, player=action.player):
          actions.append(action.concrete_action())
          options.remove(option)
          break
    actions.reverse()

    # Add compelled actions
    for option in options:
      if option.compelled:
        instance = option.random_instance(game=game, player=option.player)
        actions.append(instance)

    # Resolve actions
    actions = sorted(actions, key=lambda action: action.precedence)
    for action in actions:
      action.resolve(state)
    for action in actions:
      action.resolve_post(state)
