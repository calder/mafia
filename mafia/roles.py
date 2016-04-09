from .actions import *
from .factions import *
from . import events
from . import placeholders
from .player import *
from .virtual_actions import *

import copy
import re

class RoleBase(object):
  action         = None
  faction_action = None
  vote_action    = None

  bulletproof    = False # Immune to night kills
  kills_visitors = False # Kills anyone who visits them
  lynchable      = True  # Immune to lynching
  vengeful       = False # Takes down killers with them
  visible        = True  # Whether the role shows up to trackers, watchers, and forensic investigators
  votes          = 1     # The number of votes the player gets during the day

  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.faction       = faction
    self.adjectives    = []
    self.fake_factions = []

  @property
  def apparent_factions(self):
    return [self.faction] + self.fake_factions

  @property
  def alignment(self):
    return self.faction.alignment

  @property
  def apparent_alignment(self):
    return self.alignment

  @property
  def wins_exclusively(self):
    return self.faction.wins_exclusively

  def fate(self, game):
    return self.faction.fate(game)

  def on_killed(self, **kwargs):
    pass

  def on_visited(self, **kwargs):
    pass

class Role(object):
  def __init__(self, faction_or_role):
    if isinstance(faction_or_role, Faction):
      faction_or_role = RoleBase(faction_or_role)
    assert isinstance(faction_or_role, Role) or isinstance(faction_or_role, RoleBase)
    self.base = faction_or_role

    # Prevent accidental modification of a class's prototypical action
    self.action         = copy.deepcopy(self.action)
    self.faction_action = copy.deepcopy(self.faction_action)
    self.vote_action    = copy.deepcopy(self.vote_action)

  def __str__(self):
    return "%s %s" % (self.faction.adjective, self.adjective)

  def __getattr__(self, attr):
    return getattr(self.base, attr)

  @property
  def adjectives(self):
    return re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__) + self.base.adjectives

  @property
  def adjective(self):
    return " ".join(self.adjectives)

class ActionDoubler(Role):
  action = Double(placeholders.Self(), placeholders.Player())

class Bodyguard(Role):
  action = Guard(placeholders.Self(), placeholders.Other())
  elite_bodyguard = False

class Bulletproof(Role):
  bulletproof = True

class EliteBodyguard(Bodyguard):
  elite_bodyguard = True

class Busdriver(Role):
  action = Busdrive(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Cop(Role):
  action = Investigate(placeholders.Self(), placeholders.Player())

class Delayer(Role):
  action = Delay(placeholders.Self(), placeholders.Player())

class Doctor(Role):
  action = Protect(placeholders.Self(), placeholders.Player())

class DoubleVoter(Role):
  votes = 2

class ForensicInvestigator(Role):
  action = Autopsy(placeholders.Self(), placeholders.Corpse())

class Goon(Role):
  faction_action = Kill(placeholders.Self(), placeholders.Player())

class Godfather(Goon):
  apparent_alignment = Alignment.good

class Governor(Role):
  vote_action = Pardon(placeholders.Self, placeholders.Other(), visible=False)

class Hitman(Role):
  faction_action = Kill(placeholders.Self(), placeholders.Player(), protectable=placeholders.Bool(default=False))

class Joker(Role):
  def __init__(self, faction=None):
    faction = faction or JokerFaction("Joker")
    super().__init__(faction)

class Lyncher(Role):
  def __init__(self, lynchee_or_lyncher_faction):
    if isinstance(lynchee_or_lyncher_faction, Player):
      faction_name = "%s Lyncher" % lynchee_or_lyncher_faction
      faction = LyncherFaction(faction_name, lynchee_or_lyncher_faction)
    else:
      faction = lynchee_or_lyncher_faction
    super().__init__(faction)

class Mason(Role):
  pass

class Miller(Role):
  apparent_alignment = Alignment.evil

class Ninja(Role):
  visible = False

class Overeager(Role):
  def __init__(self, base):
    super().__init__(base)
    if base.action: self.action = Compelled(base.action)

class ParanoidGunOwner(Role):
  def on_visited(self, *, game, player, by):
    self.base.on_visited(game=game, player=player, by=by)
    Kill(player, by)._resolve(game)

class Politician(Role):
  action = StealVote(placeholders.Self(), placeholders.Player())

class Roleblocker(Role):
  action = Roleblock(placeholders.Self(), placeholders.Player())

class Tracker(Role):
  action = Track(placeholders.Self(), placeholders.Player())

class Unlynchable(Role):
  unlynchable = True

class Usurper(Role):
  def __init__(self, faction, usurpee):
    super().__init__(faction)
    self.usurpee = usurpee

  def fate(self, game):
    faction_fate = self.faction.fate(game)
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  action = Watch(placeholders.Self(), placeholders.Player())

class Vengeful(Role):
  def on_killed(self, *, game, player, by):
    self.base.on_killed(game=game, player=player, by=by)
    Kill(player, by)._resolve(game)

class Ventriloquist(Role):
  action = Possess(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Vigilante(Role):
  action = Kill(placeholders.Self(), placeholders.Player())

class Villager(Role):
  pass
