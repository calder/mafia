class Phase(object):
  def resolve(self, game):
    assert game.log.current_phase == self, \
           "Use Game.resolve rather than calling resolve directly."

    self._resolve(game)

    # Remove expired effects
    for player in game.all_players:
      for effect in player.effects:
        effect.expiration.advance(self)
      player.effects = [e for e in player.effects if not e.expired]

  def _resolve(self, game):
    pass
