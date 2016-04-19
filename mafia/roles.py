from .actions import *
from .factions import *
from . import effects
from . import events
from .mixin import *
from . import placeholders
from .player import *
from .virtual_actions import *

import re

class RoleBase(object):
  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self.mixins         = []
    self._faction       = faction
    self._fake_factions = []

  def __str__(self):
    return "%s %s" % (self.faction.adjective, self.adjective)

  def add_mixin(self, effect):
    self.mixins.append(effect)

  @mixin("mixins")
  def action(self):
    return None

  @mixin("mixins")
  def adjective(self):
    return " ".join(self.adjectives)

  @mixin("mixins")
  def adjectives(self):
    return []

  @mixin("mixins")
  def apparent_factions(self):
    return [self.faction] + self.fake_factions

  @mixin("mixins")
  def alignment(self):
    return self.faction.alignment

  @mixin("mixins")
  def apparent_alignment(self):
    return self.alignment

  @mixin("mixins")
  def faction(self):
    return self._faction

  @mixin("mixins")
  def faction_action(self):
    return None

  @mixin("mixins")
  def fake_factions(self):
    return self._fake_factions

  @mixin("mixins")
  def fate(self):
    return self.faction.fate

  @mixin("mixins")
  def is_town_enemy(self):
    return self.faction.is_town_enemy

  @mixin("mixins")
  def is_town_friend(self):
    return self.faction.is_town_friend

  @mixin_fn("mixins")
  def on_killed(self, *, game, player, **kwargs):
    game.log.append(events.Died(player))
    player.add_effect(effects.Dead())

  @mixin_fn("mixins")
  def on_lynched(self, *, game, player, **kwargs):
    game.log.append(events.Lynched(player))
    player.add_effect(effects.Dead())

  @mixin_fn("mixins")
  def on_visited(self, **kwargs):
    pass

  @mixin("mixins")
  def visible(self):
    return True

  @mixin("mixins")
  def vote_action(self):
    return None

  @mixin("mixins")
  def votes(self):
    return 1

  @mixin("mixins")
  def wins_exclusively(self):
    return self.faction.wins_exclusively

class Role(object):
  def __new__(cls, faction_or_role, *args, **kwargs):
    if isinstance(faction_or_role, Faction):
      base = RoleBase(faction_or_role)
    else:
      base = faction_or_role
    assert isinstance(base, RoleBase)

    obj = super(Role, cls).__new__(cls)
    obj.__init__(*args, **kwargs)
    base.add_mixin(obj)
    for e in obj.starting_effects: base.add_mixin(e)
    return base

  def adjectives_fn(self, base):
    return re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__) + base()

  @property
  def starting_effects(self):
    return []

class ActionDoubler(Role):
  @property
  def action(self):
    return Double(placeholders.Self(), placeholders.Player())

class Bodyguard(Role):
  @property
  def action(self):
    return Guard(placeholders.Self(), placeholders.Other())

class Bulletproof(Role):
  def on_killed_fn(self, base, *, game, player, by, protectable, **kwargs):
    if protectable: game.log.append(events.Protected(player))
    else:           return base()

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

class EliteBodyguard(Role):
  @property
  def action(self):
    return EliteGuard(placeholders.Self(), placeholders.Other())

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
    return HitmanKill(placeholders.Self(), placeholders.Player())

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
  def action_fn(self, base):
    base = base()
    if base: return Compelled(base)

class ParanoidGunOwner(Role):
  def on_visited_fn(self, base, *, game, player, by):
    base()
    resolve_kill(player, by, game=game)

class Politician(Role):
  @property
  def action(self):
    return StealVote(placeholders.Self(), placeholders.Player())

class Roleblocker(Role):
  @property
  def action(self):
    return Roleblock(placeholders.Self(), placeholders.Player())

class Stone(Role):
  @property
  def starting_effects(self):
    return [effects.Stoned()]

class Tracker(Role):
  @property
  def action(self):
    return Track(placeholders.Self(), placeholders.Player())

class Unlynchable(Role):
  def on_lynched_fn(self, base, *, game, player):
    game.log.append(events.NoLynch())

class Usurper(Role):
  def __init__(self, usurpee):
    self.usurpee = usurpee

  def fate_fn(self, base):
    faction_fate = base()
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  @property
  def action(self):
    return Watch(placeholders.Self(), placeholders.Player())

class Vengeful(Role):
  def on_killed_fn(self, base, *, game, player, by, **kwargs):
    base()
    resolve_kill(player, by, game=game)

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
