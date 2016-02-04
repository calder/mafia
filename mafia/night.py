from .log import *
from .phase import *
from .util import *
from .virtual_actions import *

class Night(Phase):
  """
  A single night in a Mafia game.

  Usage:
    night0 = Night(0)
    night0.add_action(Investigate(cop, goon))
    night0.add_action(FactionAction(mafia, Kill(cop, goon)))
    game.resolve(night0)
  """

  def __init__(self, number):
    self.number      = number
    self.raw_actions = []

  def __str__(self):
    return "Night %d" % self.number

  def add_action(self, action):
    self.raw_actions.append(action)

  def _resolve(self, game):
    # Compile valid action set
    options = set()
    for player in game.players:
      for action in player.role.actions:
        for i in range(player.action_count):
          options.add(player.role.action.with_player(player))
    del player  # Avoid confusion if used
    for faction in game.factions:
      if faction.action:
        options.add(FactionAction(faction, faction.action))
    del faction  # Avoid confusion if used

    # Check actions
    actions = []
    for action in reversed(self.raw_actions):
      for option in options:
        if option.matches(action, game=game, player=action.player):
          actions.append(action.concrete_action())
          options.remove(option)
          break
    actions.reverse()

    # Add compelled actions
    for option in options:
      if option.compelled:
        instance = option.random_instance(game=game, player=option.player)
        actions.append(instance)

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
