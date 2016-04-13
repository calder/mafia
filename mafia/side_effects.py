from . import events

def resolve_kill(player, target, *, game, protectable=True):
  # Skip redundant kills
  if not target.alive:
    return

  # Kill the victim
  target.on_killed(game=game, player=target, by=player, protectable=protectable)
