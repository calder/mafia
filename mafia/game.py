from .log import *
from .factions import *
from .player import *
from .roles import Role
from .util import *

import random

EVERYONE_LOST = SingletonValue()
NO_WINNER_YET = SingletonValue()

class Game(object):
  """
  A single game of Mafia.

  Usage:
    game  = Game()
    town  = game.add_faction(Town())
    mafia = game.add_faction(Mafia("The Sopranos"))
    alice = game.add_player("Alice", Cop(town))
    bob   = game.add_player("Bob", Doctor(town))
    eve   = game.add_player("Eve", Goon(mafia))

    night0 = Night(0)
    night0.add_action(Investigate(alice, eve))
    night0.add_action(Protect(bob, alice))
    night0.add_action(FactionAction(mafia, Kill(eve, alice)))
    game.resolve(night0)

    day1 = Day(1)
    day1.set_vote(alice, eve)
    day1.set_vote(eve, alice)
    day1.set_vote(bob, eve)
    game.resolve(day1)
  """

  def __init__(self, seed=42):
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
    Add a player to the game and return it.

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

  def begin(self):
    """Send out roles and teammates."""
    for player in self.players:
      self.log.append(events.RoleAnnouncement(player, player.role))

    for faction in self.factions:
      members = faction.apparent_members(self)
      if members and len(members) > 1:
        self.log.append(events.FactionAnnouncement(faction, members))

  def resolve(self, phase):
    self.log.current_phase = phase
    phase.resolve(self)

  @property
  def players(self):
    return sorted([player for player in self.all_players.values() if player.alive])

  @property
  def factions(self):
    return sorted(list(set([p.faction for p in self.players])))

  def winners(self):
    fates = {p: p.fate(self) for p in self.all_players.values()}
    winners   = sorted([f for f in fates if fates[f] is Fate.won])
    undecided = sorted([f for f in fates if fates[f] is Fate.undecided])
    losers    = sorted([f for f in fates if fates[f] is Fate.lost])

    if   len(winners)   > 0: return winners
    elif len(undecided) > 0: return NO_WINNER_YET
    else:                    return EVERYONE_LOST

  def shuffled(self, list):
    """Return a deterministically shuffled version of the given list."""

    shuffled = sorted(list)
    self.random.shuffle(shuffled)
    return shuffled
