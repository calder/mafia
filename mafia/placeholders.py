from .player import *

class Placeholder(object):
  class Placeholder(object):
    def __str__(self):
      return self.__class__.__name__

  class AnyPlayer(Placeholder):
    def matches(self, other, **kwargs):
      return isinstance(other, Player) and other.alive

    def random_instance(self, *, game, **kwargs):
      return game.random.choice(game.live_players)

  class FactionMember(AnyPlayer):
    def __init__(self, faction):
      self.faction = faction

    def __str__(self):
      return "%s(%s)" % (self.__class__.__name__, self.faction.name)

    def matches(self, other, **kwargs):
      return super().matches(other, **kwargs) and other.role.faction == self.faction

    def random_instance(self, *, game, **kwargs):
      players = filter(lambda p: p.faction == self.faction, game.live_players)
      return game.random.choice(players)

  class PlayerExcept(AnyPlayer):
    def __init__(self, exclude):
      self.exclude = exclude

    def random_instance(self, *, game, player):
      players = game.live_players
      if player in players: players.remove(player)
      return game.random.choice(players)

  class Self(AnyPlayer):
    def matches(self, other, *, player, **kwargs):
      return super().matches(other, player=player, **kwargs) and other == player

    def random_instance(self, *, player, **kwargs):
      return player

  class Corpse(Placeholder):
    def matches(self, other, *, player, **kwargs):
      return isinstance(other, Player) and other.alive is False
