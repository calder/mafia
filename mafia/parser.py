import copy
import functools
import re

from .day import *
from .night import *

class Command(object):
  def __init__(self, pattern, command, *, help=None, phase=None):
    self.help    = help or pattern
    self.pattern = pattern
    self.command = command
    self.phase   = phase

    pattern = pattern.replace("<PLAYER>", r"(\w+)")
    pattern = pattern.replace("<TEXT>", r"(.*)")
    self.regex = re.compile(pattern, re.DOTALL + re.IGNORECASE)

# TODO: Generalize.
class Parser(object):
  def __init__(self, game):
    self.game = game
    self.commands = [
      Command(r"\s*(?:vote|lynch) <PLAYER>.*?", self.update_vote, phase=Day,
              help="vote <PLAYER>"),
      Command(r"\s*unvote|(?:cancel|clear|delete|retract|undo) vote.*?", self.clear_vote, phase=Day,
              help="unvote"),
      Command(r"\s*(?:leave|set|update|write) will:?<TEXT>", self.update_will,
              help="set will:\n..."),
    ]

  def parse(self, phase, player, message):
    for command in self.get_commands(player):
      match = command.regex.fullmatch(message)
      if match:
        if command.phase and not isinstance(phase, command.phase):
          raise WrongPhase(right_phase=command.phase)
        return command.command(phase, player, *match.groups())
    raise InvalidAction()

  def get_commands(self, player, *, phase=None):
    commands = copy.copy(self.commands)
    if player.action:
      commands.append(self.get_action_command(player.action))
    if player.faction.leader(game=self.game) == player:
      for member in player.faction.members(game=self.game):
        if member.faction_action:
          commands.append(self.get_faction_action_command(player.faction, member.faction_action))
    if phase:
      commands = [c for c in commands if isinstance(c.phase, phase)]
    return commands

  def get_action_command(self, action):
    targets = " ".join(["<PLAYER>" for t in action.targets])
    pattern = "%s %s" % (action.name, targets)
    return Command(pattern, self.perform_action(action), phase=Night)

  def get_faction_action_command(self, faction, action):
    command = self.get_action_command(action)
    pattern = "%s: %s" % (action.player.unique_name, command.pattern)
    return Command(pattern, self.perform_faction_action(faction, action), phase=Night)

  def get_help(self, player, *, phase=None):
    return [c.help for c in self.get_commands(player, phase=phase)]

  def get_player(self, name):
    player = self.game.player_named(name)
    if not player:
      raise InvalidPlayer(name)
    return player

  def clear_vote(self, phase, player):
    phase.set_vote(player, None)

  def perform_action(self, action):
    def inner(phase, player, *targets):
      targets = [self.get_player(player) for player in targets]
      real_action = action.with_targets(targets)
      if not action.matches(real_action):
        raise IllegalAction()
      phase.add_action(real_action)
    return inner

  def perform_faction_action(self, faction, action):
    def inner(phase, player, *targets):
      targets = [self.get_player(player) for player in targets]
      phase.add_action(FactionAction(faction, action.with_targets(targets)))
    return inner

  def update_vote(self, phase, player, vote):
    phase.set_vote(player, self.get_player(vote))

  def update_will(self, phase, player, will):
    player.will = will.strip()
