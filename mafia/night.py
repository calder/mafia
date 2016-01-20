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
    action_map = defaultdict(list)
    for player in game.players.values():
      template = player.role.action.with_player(player)
      raw, action = template.select_action(self.raw_actions, game=game, player=player)
      if action: action_map[raw].append(action)
    for faction in game.factions.values():
      template = FactionAction(faction, faction.action)
      raw, action = template.select_action(self.raw_actions, game=game, player=player)
      if action: action_map[raw].append(action)
    self.actions = []
    for raw in self.raw_actions:
      self.actions += action_map[raw]
    self.actions += action_map[None]

    # Resolve actions
    self.actions = sorted(self.actions, key=lambda action: action.precedence)
    for action in self.actions:
      action.resolve(self.state)
    for action in self.actions:
      action.resolve_post(self.state)
