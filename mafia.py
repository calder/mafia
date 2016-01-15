from .actions import *
from .factions import *
from .log import *
from .night import *
from .roles import *

from collections import *
from copy import deepcopy

class Player(object):
  def __init__(self, name, *, role):
    self.name = name
    self.role = role
    self.alive = True

  def __str__(self):
    return self.name

  @property
  def alignment(self):
      return self.role.faction.alignment

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
