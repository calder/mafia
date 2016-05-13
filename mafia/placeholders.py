from . import player

class Placeholder(object):
  def __str__(self):
    return self.__class__.__name__

  @property
  def switched_with(self):
    """For printing of Actions."""
    return self

class Player(Placeholder):
  def matches(self, other, **kwargs):
    return isinstance(other, player.Player) and other.alive

  def random_instance(self, *, game, **kwargs):
    return game.random.choice(game.players)

class FactionMember(Player):
  def __init__(self, faction=None):
    self.faction = faction

  def __str__(self):
    return "%s(%s)" % (self.__class__.__name__, self.faction)

  def matches(self, other, **kwargs):
    return super().matches(other, **kwargs) and other.faction == self.faction

  def random_instance(self, *, game, **kwargs):
    return game.random.choice(self.faction.players(game.players))

class Other(Player):
  def matches(self, other, *, player, **kwargs):
    return super().matches(other) and other != player

class Self(Player):
  def matches(self, other, *, player, **kwargs):
    return other == player

class Corpse(Placeholder):
  def matches(self, other, **kwargs):
    return isinstance(other, player.Player) and not other.alive
