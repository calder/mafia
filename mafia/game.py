from .log import *
from .factions import *
from .player import *
from .roles import RoleBase
from .util import *

import random

EVERYONE_LOST = SingletonValue("EVERYONE_LOST")
NO_WINNER_YET = SingletonValue("NO_WINNER_YET")

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

  def __init__(self, *, seed=42):
    self.random          = random.Random(seed)
    self.log             = Log()
    self.faction_dict    = {}
    self.player_dict     = {}
    self.delayed_actions = []

  def add_faction(self, faction):
    assert faction.name not in self.faction_dict

    faction.game = self
    self.faction_dict[faction.name] = faction
    return faction

  def add_player(self, player, role=None):
    """
    Add a player to the game and return it.

    Takes either a single Player object, or a name and role from which to
    construct a Player object.
    """

    if role:
      assert isinstance(role, RoleBase)
      player = Player(player, role)

    assert isinstance(player, Player)
    assert player.name not in self.player_dict

    self.player_dict[player.name] = player
    return player

  def begin(self):
    """Send out roles and teammates."""
    for player in self.players:
      self.log.append(events.RoleAnnouncement(player, player.role))

    for faction in self.factions:
      members = faction.apparent_members
      if members and len(members) > 1:
        self.log.append(events.FactionAnnouncement(faction, members))

  def resolve(self, phase):
    self.log.current_phase = phase
    phase.resolve(self)

  @property
  def players(self):
    return [p for p in self.all_players if p.alive]

  @property
  def all_players(self):
    return sorted([player for player in self.player_dict.values()])

  @property
  def factions(self):
    return sorted(set([p.faction for p in self.players]))

  @property
  def all_factions(self):
    return sorted(set([p.faction for p in self.all_players]))

  def winners(self):
    fates = {p: p.fate for p in self.all_players}
    winners   = sorted([f for f in fates if fates[f] is Fate.won])
    undecided = sorted([f for f in fates if fates[f] is Fate.undecided])
    losers    = sorted([f for f in fates if fates[f] is Fate.lost])

    if   len(winners)   > 0: return winners
    elif len(undecided) > 0: return NO_WINNER_YET
    else:                    return EVERYONE_LOST

  def is_game_over(self):
    winners = self.winners()
    if winners == NO_WINNER_YET: return False
    if winners == EVERYONE_LOST: return True
    return any([p.wins_exclusively for p in winners])

  def shuffled(self, list):
    """Return a deterministically shuffled version of the given list."""

    shuffled = sorted(list)
    self.random.shuffle(shuffled)
    return shuffled
