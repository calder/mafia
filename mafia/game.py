from .log import *
from .factions import *
from .player import *
from .roles import Role
from .util import *

import random

EVERYONE_LOST = SingletonValue("EVERYONE_LOST")
NO_WINNER_YET = SingletonValue("NO_WINNER_YET")

START = SingletonValue("Start")

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
    game.begin()

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

  def __init__(self, name=None, *, seed=42):
    self.name            = name
    self.random          = random.Random(seed)
    self.log             = Log()
    self.faction_list    = []
    self.faction_names   = {}
    self.player_list     = []
    self.player_names    = {}
    self.delayed_actions = []

  def add_faction(self, faction):
    assert faction.name.lower() not in self.faction_names
    faction.game = self
    self.faction_list.append(faction)
    self.faction_names[faction.name.lower()] = faction
    return faction

  def add_player(self, player, role=None, **kwargs):
    """
    Add a player to the game and return it.

    Takes either a single Player object, or a name and role from which to
    construct a Player object.
    """

    if role:
      assert isinstance(role, Role)
      player = Player(player, role, **kwargs)
    else:
      assert isinstance(player, Player)
      assert len(kwargs) == 0

    assert player.name.lower() not in self.player_names
    self.player_list.append(player)
    self.player_names[player.name.lower()] = player
    return player

  def begin(self):
    """Send out roles and teammates."""
    self.log.current_phase = START

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
    return sorted(self.player_list)

  def player_named(self, name):
    """Return a player with the given name (case insensitive) or None."""
    return self.player_names.get(name, None)

  @property
  def factions(self):
    return sorted(set([p.faction for p in self.players]))

  def faction_named(self, name):
    """Return a faction with the given name (case insensitive) or None."""
    return self.faction_names.get(name, None)

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
