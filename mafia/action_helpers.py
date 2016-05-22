import mafia

def resolve_death(player, *, game):
  old_faction_leader = player.faction.leader(game=game)

  # Kill the player
  player.add_effect(mafia.effects.Dead())

  # Send promotion to new faction leader if necessary
  new_faction_leader = player.faction.leader(game=game)
  if new_faction_leader != old_faction_leader and player.faction.action(game=game):
     game.log.append(mafia.events.FactionLeaderAnnouncement(player.faction, new_faction_leader))

def resolve_kill(player, target, *, game, protectable=True, stack=None):
  # Skip redundant kills
  if not target.alive:
    return

  # Prevent infinite bodyguarding loops
  stack = stack or []
  if target in stack:
    protectable = False
  stack = stack + [target]

  # Resolve the kill
  target.on_killed(game=game, player=target, by=player, protectable=protectable, stack=stack)
