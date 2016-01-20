from .log import *
from .util import *
from .virtual_actions import *

import copy

class NightState(object):
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
  def __init__(self, number):
    self.number      = number
    self.raw_actions = []

    # Resolution state
    self.state       = None
    self.actions     = None

  def __str__(self):
    return "Night %d" % self.number

  def add_action(self, action):
    self.raw_actions.append(action)

  def resolve(self, game):
    self.state = NightState(self, game)

    # Check actions
    actions = {}
    for player in game.players.values():
      template = player.role.action.with_player(player)
      raw_action, action = template.select_action(game, player, self.raw_actions)
      actions[raw_action] = action
    for faction in game.factions.values():
      template = FactionAction(faction, faction.action)
      raw_action, action = template.select_action(game, player, self.raw_actions)
      actions[raw_action] = action
    self.actions = [actions[a] for a in self.raw_actions if a in actions]
    del actions

    # Resolve actions
    self.actions = sorted(self.actions, key=lambda action: action.precedence)
    for action in self.actions:
      action.resolve(self.state)
    for action in self.actions:
      action.resolve_post(self.state)
