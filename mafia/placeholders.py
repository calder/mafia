from .player import *

class Placeholder(object):
  class Placeholder(object):
    def __str__(self):
      return self.__class__.__name__

  class Corpse(Placeholder):
    def matches(self, other, *, game, player):
      return isinstance(other, Player) and other.alive is False

  class Player(Placeholder):
    def matches(self, other, *, game, player):
      return isinstance(other, Player) and other.alive

    def fill_randomly(self, *, game, player):
      return game.random.choice(game.live_players)

  class FactionMember(Player):
    def __init__(self, faction):
      self.faction = faction

    def __str__(self):
      return "%s(%s)" % (self.__class__.__name__, self.faction.name)

    def matches(self, other, **kwargs):
      return super().matches(other, **kwargs) and other.role.faction == self.faction

    def fill_randomly(self, *, game, player):
      players = filter(lambda p: p.faction == self.faction, game.live_players)
      return game.random.choice(players)

  class PlayerExcept(Player):
    def __init__(self, exclude):
      self.exclude = exclude

    def fill_randomly(self, *, game, player):
      players = game.live_players
      if player in players: players.remove(player)
      return game.random.choice(players)

  class Self(Player):
    def matches(self, other, *, game, player):
      return other == player

    def fill_randomly(self, *, game, player):
      return player
