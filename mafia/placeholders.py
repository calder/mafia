from . import player

class Placeholder(object):
  class Placeholder(object):
    def __eq__(self, other):
      return self.matches(other)

    def __str__(self):
      return self.__class__.__name__

  class Player(Placeholder):
    def matches(self, other):
      return isinstance(other, player.Player) and other.alive

  class Self(Player):
    pass

  class FactionMember(Player):
    def __init__(self, faction):
      self.faction = faction

    def __str__(self):
      return "%s(%s)" % (self.__class__.__name__, self.faction.name)

    def matches(self, other):
      return super().matches(other) and other.role.faction == self.faction

  class PlayerExcept(Player):
    def __init__(self, exclude):
      self.exclude = exclude

  class Corpse(Placeholder):
    def matches(self, other):
      return isinstance(other, player.Player) and other.alive is False
