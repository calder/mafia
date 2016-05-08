from .actions import *
from .factions import *
from . import effects
from . import events
from . import placeholders
from .player import *
from .virtual_actions import *

import re

class RoleBase(object):
  def __init__(self, faction):
    assert isinstance(faction, Faction)
    self._faction       = faction
    self._fake_factions = []

  @property
  def action(self):
    return None

  @property
  def adjectives(self):
    return []

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
  def faction(self):
    return self._faction

  @property
  def faction_action(self):
    return None

  @property
  def fake_factions(self):
    return self._fake_factions

  @property
  def fate(self):
    return self.faction.fate

  @property
  def is_town_enemy(self):
    return self.faction.is_town_enemy

  @property
  def is_town_friend(self):
    return self.faction.is_town_friend

  def on_killed(self, *, game, player, **kwargs):
    game.log.append(events.Died(player))
    player.add_effect(effects.Dead())

  def on_lynched(self, *, game, player, **kwargs):
    game.log.append(events.Lynched(player))
    player.add_effect(effects.Dead())

  def on_visited(self, **kwargs):
    pass

  @property
  def visible(self):
    return True

  @property
  def vote_action(self):
    return None

  @property
  def votes(self):
    return 1

  @property
  def wins_exclusively(self):
    return self.faction.wins_exclusively

class Role(object):
  def __init__(self, faction_or_role):
    if isinstance(faction_or_role, Faction):
      self.base = RoleBase(faction_or_role)
    else:
      self.base = faction_or_role

  def __getattr__(self, attr):
    if attr == "base":
      raise AttributeError

    return getattr(self.base, attr)

  def __str__(self):
    return "%s %s" % (self.faction.adjective, self.adjective)

  @property
  def adjective(self):
    return " ".join(self.adjectives)

  @property
  def adjectives(self):
    return re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__) + self.base.adjectives

class ActionDoubler(Role):
  @property
  def action(self):
    return Double(placeholders.Self(), placeholders.Player())

class Bodyguard(Role):
  @property
  def action(self):
    return Guard(placeholders.Self(), placeholders.Other())

class Bulletproof(Role):
  def on_killed(self, *, game, player, protectable, **kwargs):
    if protectable:
      game.log.append(events.Protected(player))
    else:
      self.base.on_killed(game=game, player=player,
                          protectable=protectable, **kwargs)

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

class Miller(Role):
  @property
  def apparent_alignment(self):
    return Alignment.evil

class Ninja(Role):
  @property
  def visible(self):
    return False

class Overeager(Role):
  @property
  def action(self):
    if self.base.action:
      return Compelled(self.base.action)

class ParanoidGunOwner(Role):
  def on_visited(self, *, game, player, by):
    resolve_kill(player, by, game=game)

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
  def on_lynched(self, *, game, player):
    game.log.append(events.NoLynch())

class Usurper(Goon):
  def __init__(self, faction_or_role, usurpee):
    super().__init__(faction_or_role)
    self.usurpee = usurpee

  @property
  def fate(self):
    faction_fate = self.base.fate
    if faction_fate is Fate.won:
      return Fate.lost if self.usurpee.alive else Fate.won
    return faction_fate

class Watcher(Role):
  @property
  def action(self):
    return Watch(placeholders.Self(), placeholders.Player())

class Vengeful(Role):
  def on_killed(self, *, game, player, by, protectable, **kwargs):
    self.base.on_killed(game=game, player=player, by=by,
                        protectable=protectable, **kwargs)
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
