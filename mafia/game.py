from .log import *

class Game(object):
  def __init__(self):
    self.factions = {}
    self.players = {}
    self.log = Log()

  def add_faction(self, faction):
    assert faction.name not in self.factions
    self.factions[faction.name] = faction
    return faction

  def add_player(self, player):
    assert player.name not in self.players
    self.players[player.name] = player
    return player

  def resolve(self, phase):
    phase.resolve(self)
