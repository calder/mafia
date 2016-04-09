from .mixin import *

class Player(object):
  def __init__(self, name, role):
    super().__init__()
    self.name    = name
    self.role    = role
    self.alive   = True
    self.effects = []

  def __str__(self):
    return self.name

  def __lt__(self, other):
    return self.name < other.name

  def matches(self, other, **kwargs):
    return self == other

  def add_effect(self, effect):
    self.effects.append(effect)

  @property
  def action(self):
    if self.role.action: return self.role.action.with_player(self)

  @property
  def alignment(self):
    return self.role.alignment

  @property
  def apparent_factions(self):
    return self.role.apparent_factions

  @property
  def apparent_alignment(self):
    return self.role.apparent_alignment

  @property
  def elite_bodyguard(self):
    return self.role.elite_bodyguard

  @property
  def faction_action(self):
    if self.role.faction_action: return self.role.faction_action.with_player(self)

  @property
  def faction(self):
    return self.role.faction

  @property
  def vengeful(self):
    return self.role.vengeful

  @property
  def vote_action(self):
    if self.role.vote_action: return self.role.vote_action.with_player(self)

  @property
  def votes(self):
    return self.role.votes

  @property
  def wins_exclusively(self):
    return self.role.wins_exclusively

  def fate(self, game):
    return self.role.fate(game)

  def on_killed(self, **kwargs):
    return self.role.on_killed(player=self, **kwargs)

  def on_visited(self, **kwargs):
    return self.role.on_visited(player=self, **kwargs)


  ###   Overridable by Effects   ###

  @mixin("effects")
  def action_count(self):
    return 1 + sum([getattr(m, "extra_actions", 0) for m in self.effects])

  @mixin("effects")
  def blocked(self): return False

  @mixin("effects")
  def delayed(self): return False

  @mixin("effects")
  def guarded_by(self): return None

  @mixin("effects")
  def must_target(self): return None

  @mixin("effects")
  def bulletproof(self): return self.role.bulletproof

  @mixin("effects")
  def lynchable(self): return self.role.lynchable

  @mixin("effects")
  def switched_with(self): return self

  @mixin("effects")
  def votes_with(self): return self
