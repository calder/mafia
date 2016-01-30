class Player(object):
  def __init__(self, name, role):
    self.name    = name
    self.role    = role
    self.alive   = True
    self.effects = []

    # These properties should never be modified,
    # only temporarily overridden by Effects.
    self.blocked       = False
    self.must_target   = None
    self.protected     = False
    self.switched_with = self
    self.votes_with    = self

  def __str__(self):
    return self.name

  def __lt__(self, other):
    return self.name < other.name

  def __getattribute__(self, name):
    if name != "effects":
      for effect in self.effects:
        if hasattr(effect, name):
          return getattr(effect, name)
    return super().__getattribute__(name)

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
