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

  def add_effect(self, effect):
    self.effects.append(effect)

  @property
  def faction(self):
    return self.role.faction

  @property
  def apparent_factions(self):
    return self.role.apparent_factions

  @property
  def alignment(self):
    return self.role.alignment

  @property
  def votes(self):
    return self.role.votes

  def matches(self, other, **kwargs):
    return self == other


  ###   Overridable by Effects   ###

  @mixin("effects")
  def actions(self):
    return 1 + sum_present(self.effects, "extra_actions")

  @mixin("effects")
  def blocked(self): return False

  @mixin("effects")
  def must_target(self): return None

  @mixin("effects")
  def protected(self): return False

  @mixin("effects")
  def switched_with(self): return self

  @mixin("effects")
  def votes_with(self): return self
