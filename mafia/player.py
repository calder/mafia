from .mixin import *

class Player(object):
  def __init__(self, name, role):
    super().__init__()
    self.name    = name
    self.effects = []

    # TODO: Make these use effects.
    self.role    = role
    self.alive   = True

  def __str__(self):
    return self.name

  def __lt__(self, other):
    return self.name < other.name

  def matches(self, other, **kwargs):
    return self == other

  def add_effect(self, effect):
    self.effects.append(effect)

  @mixin("effects")
  def action(self):
    if self.role.action:
      return self.role.action.with_player(self)

  @mixin("effects")
  def action_count(self):
    return 1

  @mixin("effects")
  def alignment(self):
    return self.role.alignment

  @mixin("effects")
  def apparent_alignment(self):
    return self.role.apparent_alignment

  @mixin("effects")
  def apparent_factions(self):
    return self.role.apparent_factions

  @mixin("effects")
  def blocked(self):
    return False

  @mixin("effects")
  def bulletproof(self):
    return self.role.bulletproof

  @mixin("effects")
  def delayed(self):
    return False

  @mixin("effects")
  def elite_guarded(self):
    return False

  @mixin("effects")
  def faction_action(self):
    if self.role.faction_action:
      return self.role.faction_action.with_player(self)

  @mixin("effects")
  def faction(self):
    return self.role.faction

  @mixin_fn("effects")
  def fate(self, game):
    return self.role.fate(game)

  @mixin("effects")
  def guarded_by(self):
    return None

  @mixin("effects")
  def lynchable(self):
    return self.role.lynchable

  @mixin("effects")
  def must_target(self):
    return None

  @mixin_fn("effects")
  def on_killed(self, **kwargs):
    return self.role.on_killed(player=self, **kwargs)

  @mixin_fn("effects")
  def on_visited(self, **kwargs):
    return self.role.on_visited(player=self, **kwargs)

  @mixin("effects")
  def switched_with(self):
    return self

  @mixin("effects")
  def vengeful(self):
    return self.role.vengeful

  @mixin("effects")
  def vote_action(self):
    if self.role.vote_action:
      return self.role.vote_action.with_player(self)

  @mixin("effects")
  def votes(self):
    return self.role.votes

  @mixin("effects")
  def votes_with(self):
    return self

  @mixin("effects")
  def wins_exclusively(self):
    return self.role.wins_exclusively
