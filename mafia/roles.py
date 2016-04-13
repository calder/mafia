from .actions import *
from .factions import *
from . import events
from .mixin import *
from . import placeholders
from .player import *
from .virtual_actions import *

import copy
import re

class RoleBase(object):
  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.adjectives     = []
    self.effects        = []
    self._faction       = faction
    self._fake_factions = []

  def add_effect(self, effect):
    self.effects.append(effect)

  @mixin("effects")
  def action(self):
    return None

  @mixin("effects")
  def apparent_factions(self):
    return [self.faction] + self.fake_factions

  @mixin("effects")
  def alignment(self):
    return self.faction.alignment

  @mixin("effects")
  def apparent_alignment(self):
    return self.alignment

  @mixin("effects")
  def bulletproof(self):
    return False

  @mixin("effects")
  def faction(self):
    return self._faction

  @mixin("effects")
  def fake_factions(self):
    return self._fake_factions

  @mixin("effects")
  def wins_exclusively(self):
    return self.faction.wins_exclusively

  @mixin("effects")
  def faction_action(self):
    return None

  @mixin("effects")
  def fate(self):
    return self.faction.fate

  @mixin("effects")
  def kills_visitors(self):
    return False

  @mixin("effects")
  def lynchable(self):
    return True

  @mixin_fn("effects")
  def on_killed(self, **kwargs):
    pass

  @mixin_fn("effects")
  def on_visited(self, **kwargs):
    pass

  @mixin("effects")
  def vengeful(self):
    return False

  @mixin("effects")
  def visible(self):
    return True

  @mixin("effects")
  def vote_action(self):
    return None

  @mixin("effects")
  def votes(self):
    return 1

class Role(object):
  def __init__(self, faction_or_role):
    if isinstance(faction_or_role, Faction):
      faction_or_role = RoleBase(faction_or_role)
    assert isinstance(faction_or_role, Role) or isinstance(faction_or_role, RoleBase)
    self.base = faction_or_role

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
  @property
  def action(self):
    return Double(placeholders.Self(), placeholders.Player())

class Bodyguard(Role):
  @property
  def action(self):
    return Guard(placeholders.Self(), placeholders.Other())

class Bulletproof(Role):
  @property
  def bulletproof(self):
    return True

class EliteBodyguard(Role):
  @property
  def action(self):
    return Guard(placeholders.Self(), placeholders.Other(), elite=placeholders.Bool(default=True))

class Busdriver(Role):
  @property
  def action(self):
    return Busdrive(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Cop(Role):
  @property
  def action(self):
    return Investigate(placeholders.Self(), placeholders.Player())

class Delayer(Role):
  @property
  def action(self):
    return Delay(placeholders.Self(), placeholders.Player())

class Doctor(Role):
  @property
  def action(self):
    return Protect(placeholders.Self(), placeholders.Player())

class DoubleVoter(Role):
  @property
  def votes(self):
    return 2

class ForensicInvestigator(Role):
  @property
  def action(self):
    return Autopsy(placeholders.Self(), placeholders.Corpse())

class Goon(Role):
  @property
  def faction_action(self):
    return Kill(placeholders.Self(), placeholders.Player())

class Godfather(Goon):
  @property
  def apparent_alignment(self):
    return Alignment.good

class Governor(Role):
  @property
  def vote_action(self):
    return Pardon(placeholders.Self, placeholders.Other(), visible=False)

class Hitman(Role):
  @property
  def faction_action(self):
    return Kill(placeholders.Self(), placeholders.Player(), protectable=placeholders.Bool(default=False))

class Joker(Role):
  pass

class Lyncher(Role):
  pass

class Mason(Role):
  pass

class Miller(Role):
  @property
  def apparent_alignment(self):
    return Alignment.evil

class Ninja(Role):
  @property
  def visible(self):
    return False

class Overeager(Role):
  def __init__(self, base):
    super().__init__(base)
    if base.action: self.action = Compelled(base.action)

class ParanoidGunOwner(Role):
  def on_visited(self, *, game, player, by):
    self.base.on_visited(game=game, player=player, by=by)
    Kill(player, by)._resolve(game)

class Politician(Role):
  @property
  def action(self):
    return StealVote(placeholders.Self(), placeholders.Player())

class Roleblocker(Role):
  @property
  def action(self):
    return Roleblock(placeholders.Self(), placeholders.Player())

class Tracker(Role):
  @property
  def action(self):
    return Track(placeholders.Self(), placeholders.Player())

class Unlynchable(Role):
  @property
  def unlynchable(self):
    return True

class Usurper(Role):
  def __init__(self, faction, usurpee):
    super().__init__(faction)
    self.usurpee = usurpee

  @mixin("effects")
  def fate(self):
    faction_fate = self.faction.fate
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  @property
  def action(self):
    return Watch(placeholders.Self(), placeholders.Player())

class Vengeful(Role):
  def on_killed(self, *, game, player, by):
    self.base.on_killed(game=game, player=player, by=by)
    Kill(player, by)._resolve(game)

class Ventriloquist(Role):
  @property
  def action(self):
    return Possess(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Vigilante(Role):
  @property
  def action(self):
    return Kill(placeholders.Self(), placeholders.Player())

class Villager(Role):
  pass
