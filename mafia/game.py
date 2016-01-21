from .log import *
from .factions import *
from .player import *
from .roles import Role
from .util import *

import random

EVERYONE_LOST = SingletonValue()
NO_WINNER_YET = SingletonValue()

class Game(object):
  def __init__(self, seed):
    self.all_factions = {}
    self.all_players  = {}
    self.log          = Log()
    self.random       = random.Random(seed)

  def add_faction(self, faction):
    assert faction.name not in self.all_factions

    self.all_factions[faction.name] = faction
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
    assert player.name not in self.all_players

    self.all_players[player.name] = player
    return player

  def resolve(self, phase):
    phase.resolve(self)

  @property
  def players(self):
    return [player for player in self.all_players.values() if player.alive]

  @property
  def factions(self):
    return list(set([p.faction for p in self.players]))

  def winners(self):
    outcomes  = {f: f.fate(self.players) for f in self.factions}
    winners   = [f for f in outcomes if outcomes[f] is Fate.won]
    undecided = [f for f in outcomes if outcomes[f] is Fate.undecided]
    losers    = [f for f in outcomes if outcomes[f] is Fate.lost]

    if not len(winners) == 0: return winners
    if not len(undecided) == 0: return NO_WINNER_YET
    return EVERYONE_LOST
