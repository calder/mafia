# Architecture

At a high level, Mafia is a game where players use secret actions to manipulate each other. This library models Mafia as a game state and a variety of actions which can manipulate the state in virtually unlimited ways.

The state of a single Mafia game consists of:
 1. Players and their current liveness, role, and faction.
 2. Effects which temporarily modify players in some way.
 3. A log of events that have occurred so far in the game.

Actions may affect any component of the state. They can kill players or bring them back to life. They can swap players' roles or factions. They can temporarily make a player bulletproof, or steal their action. They can add events to the game log which may be read by other actions or sent to specific players.

Mafia games alternate between resolution of two phases: night and day. During night resolution, players' actions from the night are resolved psuedo-simultaneously following a well-defined order. During day resolution, players' votes are counted and a player is potentially lynched by the mob.

## Resolving a Night

When you call ```game.resolve(some_night)```:

 1. The log's current phase is set to ```some_night```.

 2. A set of valid action templates is compiled from the living players and factions. These are things like
    ```python
    Investigate(the_cop, placeholders.Player())
    ```
    or
    ```python
    FactionAction(the_mafia, Kill(placeholders.FactionMember(), placeholders.Player())
    ```

 3. The actions for that night are checked against the valid action set. The most recent action that matches each action template is added to a list of actions to resolve.

 4. If any compelled action templates remain in the valid action set, a random instance of the template is added to the list of actions to resolve.

 5. Any actions which were delayed from previous nights are also added to the list of actions to resolve.

 6. Actions are resolved following [Natural Action Resolution](#natural-action-resolution) order. [Reactions](#reactions) are resolved as necessary.

 7. Actions are post-resolved in the same order as they were resolved. This is only relevant to actions like watching and tracking that must occur after normal action resolution.

 8. Effect durations are decremented and expired effects are removed.

### Natural Action Resolution

Natural Action Resolution is a mostly intuitive method of choosing the order in which actions are resolved that leads to very interesting behaviors.

Under Natural Action Resolution, actions may depend on other actions. For example, Kills depend on Protects when the they share a target. Most actions depend on Roleblocks when their player is the Roleblock's target.

### Reactions

Some actions can trigger reactions. Reactions are currently hardcoded into the triggering action's resolution logic, but we might want to consider creating a more general purpose reaction framework in the future.

## Resolving a Day

Day resolution is much simpler than night resolution. When you call ```game.resolve(some_day)```:

 1. The log's current phase is set to ```some_day```.

 2. Votes are recorded after accounting for those manipulated by Politicians.

 3. [Vote actions](#vote-actions) are applied.

 4. Votes are tallied, and the player with the most votes for them is lynched.

 5. Effect durations are decremented and expired effects are removed.

### Vote Actions

Some roles have actions associated with their votes. For example, Governors automatically make the player they vote for unlynchable for a day.
