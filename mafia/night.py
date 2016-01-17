from .log import *
from .util import *

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
    self.number = number
    self.actions = []

  def __str__(self):
    return "Night %d" % self.number

  def add_action(self, action):
    self.actions.append(action)

  def ordered_actions(self):
    return sorted(self.actions, key=lambda action: action.precedence)

  def resolve(self, game):
    state = NightState(self, game)
    for action in self.ordered_actions():
      action.resolve(state)
    for action in self.ordered_actions():
      action.resolve_post(state)
