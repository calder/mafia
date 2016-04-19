from .mixin import *

class Player(object):
  def __init__(self, name, role):
    super().__init__()
    self.effects = []
    self.name    = name
    self._role   = role

  def __repr__(self):
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
  def alive(self):
    return True

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
  def delayed(self):
    return False

  @mixin("effects")
  def faction_action(self):
    if self.role.faction_action:
      return self.role.faction_action.with_player(self)

  @mixin("effects")
  def faction(self):
    return self.role.faction

  @mixin("effects")
  def fate(self):
    return self.role.fate

  @mixin("effects")
  def is_town_enemy(self):
    return self.role.is_town_enemy

  @mixin("effects")
  def is_town_friend(self):
    return self.role.is_town_friend

  @mixin("effects")
  def must_target(self):
    return None

  @mixin_fn("effects")
  def on_killed(self, **kwargs):
    return self.role.on_killed(**kwargs)

  @mixin_fn("effects")
  def on_lynched(self, **kwargs):
    return self.role.on_lynched(**kwargs)

  @mixin_fn("effects")
  def on_visited(self, **kwargs):
    return self.role.on_visited(**kwargs)

  @mixin("effects")
  def role(self):
    return self._role

  @mixin("effects")
  def switched_with(self):
    return self

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
