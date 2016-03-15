from collections import *

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

  def resolve_actions(self, actions, *, game):
    # Resolve actions using Natural Action Resolution
    actions = sorted(actions, key=lambda action: action.precedence)
    resolved_actions = []
    while len(actions) > 0:
      dependencies = defaultdict(list)

      # Try to find an action with no dependencies
      next_action = None
      for action in actions:
        dependencies[action] = [a for a in actions if action.depends_on(a)]
        if len(dependencies[action]) == 0:
          next_action = action
          break

      # If none was found, break the first loop by resolving
      # the lowest precedence action in the loop.
      if not next_action:
        chain = [actions[0]]
        while True:
          dep = dependencies[chain[-1]][0]
          if dep in chain:
            chain = chain[chain.index(dep):]
            chain.sort(key=lambda a: a.precedence, reverse=True)
            next_action = chain[-1]
            break
          chain.append(dep)

      # Resolve the action
      next_action.resolve(game)
      actions.remove(next_action)
      resolved_actions.append(next_action)

    # Post resolution. We can just do this in the same order.
    for action in resolved_actions:
      action.resolve_post(game)
