from .log import *
from .player import Player
from .roles import Role

class Game(object):
  def __init__(self):
    self.factions = {}
    self.players = {}
    self.log = Log()

  def add_faction(self, faction):
    assert faction.name not in self.factions

    self.factions[faction.name] = faction
    return faction

  def add_player(self, player, role=None):
    """
    Add a player to the game.

    Takes either a single Player object, or a name and role from which to
    construct a Player object.
    """
    if role:
      assert isinstance(role, Role)
      player = Player(player, role)

    assert isinstance(player, Player)
    assert player.name not in self.players

    self.players[player.name] = player
    return player

  def resolve(self, phase):
    phase.resolve(self)
