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
  def descriptions(self):
    return []

  @property
  def faction(self):
    return self._faction

  @property
  def faction_action(self):
    return None

  @property
  def fake_factions(self):
    return self._fake_factions

  def fate(self, **kwargs):
    return self.faction.fate(**kwargs)

  @property
  def is_town_enemy(self):
    return self.faction.is_town_enemy

  @property
  def is_town_friend(self):
    return self.faction.is_town_friend

  def on_killed(self, *, game, player, **kwargs):
    game.log.append(events.Died(player))
    resolve_death(player, game=game)

  def on_lynched(self, *, game, player, **kwargs):
    game.log.append(events.Lynched(player))
    resolve_death(player, game=game)

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

  @property
  def descriptions(self):
    return [self.description] + self.base.descriptions

  @property
  def objective(self):
    return self.faction.objective

class ActionDoubler(Role):
  description = "You may double one player each night. " \
                "That player may use their action twice the following night."

  @property
  def action(self):
    return Double(placeholders.Self(), placeholders.Player())

class Bodyguard(Role):
  description = "You may guard one player each night. " \
                "If that player is killed, you die instead of them."

  @property
  def action(self):
    return Guard(placeholders.Self(), placeholders.Other())

class Bulletproof(Role):
  description = "You cannot be killed at night."

  def on_killed(self, *, game, player, protectable, **kwargs):
    if protectable:
      game.log.append(events.Protected(player))
    else:
      self.base.on_killed(game=game, player=player,
                          protectable=protectable, **kwargs)

class Busdriver(Role):
  description = "You may busdrive two players each night. " \
                "Anyone who targets the first player will automatically " \
                "target the second player instead, and vice versa."

  @property
  def action(self):
    return Busdrive(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Cop(Role):
  description = "You may investigate one player each night. " \
                "You discover their alignment. Good means pro-town, " \
                "Evil means Mafia or Third Party."

  @property
  def action(self):
    return Investigate(placeholders.Self(), placeholders.Player())

class Delayer(Role):
  description = "You may delay one player each night. " \
                "That player's action will be resolved the following " \
                "night along with their regular action from that night."

  @property
  def action(self):
    return Delay(placeholders.Self(), placeholders.Player())

class Doctor(Role):
  description = "You may protect one player each night. " \
                "They are immune to night kills that night. " \
                "You may not protect yourself."
  @property
  def action(self):
    return Protect(placeholders.Self(), placeholders.Other())

class DoubleVoter(Role):
  description = "Your lynch vote counts as two votes."

  @property
  def votes(self):
    return 2

class EliteBodyguard(Role):
  description = "You may guard one player each night. " \
                "If that player is killed, you die instead of them. " \
                "You also kill whoever killed them."

  @property
  def action(self):
    return EliteGuard(placeholders.Self(), placeholders.Other())

class ForensicInvestigator(Role):
  description = "You may investigate one dead player each night. " \
                "You discover everyone who ever visited that player " \
                "throughout the course of the game."

  @property
  def action(self):
    return Autopsy(placeholders.Self(), placeholders.Corpse())

class Goon(Role):
  description = "You may kill one player each night, but only at " \
                "your faction leader's command."

  @property
  def faction_action(self):
    return Kill(placeholders.Self(), placeholders.Player())

class Godfather(Goon):
  description = "You appear innocent to cop investigations."

  @property
  def apparent_alignment(self):
    return Alignment.good

class Governor(Role):
  description = "Whoever you vote for during the day (except yourself) " \
                "cannot be lynched that day."

  @property
  def vote_action(self):
    return Pardon(placeholders.Self, placeholders.Other(), visible=False)

class Hitman(Role):
  description = "You may kill one player each night, but only at " \
                "your faction leader's command. They cannot be protected."

  @property
  def faction_action(self):
    return HitmanKill(placeholders.Self(), placeholders.Player())

class Joker(Role):
  description = "You have a very specific death wish."

class Lyncher(Role):
  description = "You hold a very specific grudge."

class Miller(Role):
  description = "You appear guilty to cop investigations."

  @property
  def apparent_alignment(self):
    return Alignment.evil

class Ninja(Role):
  description = "Your night actions are invisible to Trackers, Watchers, " \
                "and Forensic Investigators."

  @property
  def visible(self):
    return False

class Overeager(Role):
  description = "You MUST use your action each night. If you do not, " \
                "a target will be chosen for you at random."
  @property
  def action(self):
    if self.base.action:
      return Compelled(self.base.action)

class ParanoidGunOwner(Role):
  description = "You automatically kill any player who visits you."

  def on_visited(self, *, game, player, by):
    resolve_kill(player, by, game=game)

class Politician(Role):
  description = "You may steal one player's vote each night. " \
                "That player automatically votes with you the next day."

  @property
  def action(self):
    return StealVote(placeholders.Self(), placeholders.Player())

class Roleblocker(Role):
  description = "You may roleblock one player each night. " \
                "That player may not use their action that night."

  @property
  def action(self):
    return Roleblock(placeholders.Self(), placeholders.Player())

class Tracker(Role):
  description = "You may track one player each night. " \
                "You discover everyone they visit that night."

  @property
  def action(self):
    return Track(placeholders.Self(), placeholders.Player())

class Unlynchable(Role):
  description = "You are immune to lynching."

  def on_lynched(self, *, game, player):
    game.log.append(events.NoLynch())

class Usurper(Goon):
  description = "You win with your faction, but only if you are " \
                "its leader at the end of the game."

  def fate(self, *, player):
    faction_fate = self.base.fate(player=player)
    if faction_fate == Fate.won:
      return Fate.won if self.faction.leader == player else Fate.lost
    return faction_fate

class Watcher(Role):
  description = "You may watch one player each night. " \
                "You discover everyone who visits them that night."

  @property
  def action(self):
    return Watch(placeholders.Self(), placeholders.Player())

class Vengeful(Role):
  description = "You automatically kill anyone who kills you."

  def on_killed(self, *, game, player, by, protectable, **kwargs):
    self.base.on_killed(game=game, player=player, by=by,
                        protectable=protectable, **kwargs)
    resolve_kill(player, by, game=game)

class Ventriloquist(Role):
  description = "You may possess one player each night. " \
                "You may override their target with someone of " \
                "your choosing."

  @property
  def action(self):
    return Possess(placeholders.Self(), placeholders.Player(), placeholders.Player())

class Vigilante(Role):
  description = "You may kill one player each night."

  @property
  def action(self):
    return Kill(placeholders.Self(), placeholders.Player())

class Villager(Role):
  description = "You have no special abilities."
