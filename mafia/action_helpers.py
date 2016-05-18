import mafia

def resolve_death(player, *, game):
  old_faction_leader = player.faction.leader

  # Kill the player
  player.add_effect(mafia.effects.Dead())

  # Send promotion to new faction leader if necessary
  if old_faction_leader == player \
     and player.faction.leader \
     and player.faction.action:
     game.log.append(mafia.events.FactionLeaderAnnouncement(player.faction, player.faction.leader))

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
