from .log import *
from .factions import *
from .player import *
from .roles import Role
from .util import *

EVERYONE_LOST = SingletonValue()
NO_WINNER_YET = SingletonValue()

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

  @property
  def live_players(self):
    return [player for player in self.players.values() if player.alive]

  def winners(self):
    factions = self.factions.values()
    outcomes  = {f: f.fate(self) for f in factions}
    winners   = [f for f in outcomes if outcomes[f] is Fate.WON]
    undecided = [f for f in outcomes if outcomes[f] is Fate.UNDECIDED]
    losers    = [f for f in outcomes if outcomes[f] is Fate.LOST]

    if not len(winners) == 0: return winners
    if not len(undecided) == 0: return NO_WINNER_YET
    return EVERYONE_LOST
