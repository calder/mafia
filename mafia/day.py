from . import events
from .exceptions import *
from .log import *
import mafia.night
from .phase import *
from .util import *

from collections import *
import re

class Day(Phase):
  """
  A single day in a Mafia game.

  Usage:
    day1 = Day(1)
    day1.set_vote(cop, goon)
    day1.set_vote(goon, cop)
    day1.set_vote(villager, cop)
    game.resolve(day1)
  """

  def __init__(self, number):
    self.number     = number
    self.votes      = defaultdict(return_none)
    self.vote_order = []

  def __eq__(self, other):
    return isinstance(other, Day) and other.number == self.number

  def __str__(self):
    return "Day %d" % self.number

  def next_phase(self):
    return mafia.Night(self.number)

  def add_parsed(self, player, string, *, game):
    # Handle unvoting
    match = re.fullmatch(r"unvote|(cancel|clear|delete|retract|undo) vote", string)
    if match:
      self.set_vote(player, None)
      return

    # Handle voting
    match = re.fullmatch(r"(vote|vote for|lynch) (\w+)", string)
    if not match:
      raise MalformedVote()
    target = game.player_named(match.group(2))
    if not target:
      raise InvalidPlayer(match.group(2))
    self.set_vote(player, target)

  def set_vote(self, player, candidate):
    self.votes[player] = candidate

    # Keep track of voting order for vote action resolution
    if player in self.vote_order:
      self.vote_order.remove(player)
    self.vote_order.append(player)

  def _resolve(self, game):
    votes      = defaultdict(return_none)
    candidates = defaultdict(return_0)

    # Determine actual votes after politicianing
    for player in game.players:
      if player.votes_with.alive:
        votes[player] = self.votes[player.votes_with]

    # Apply vote actions
    vote_actions = []
    for player in self.vote_order:
      if player.vote_action:
        action = player.vote_action.with_target(votes[player])
        if player.vote_action.matches(action):
          vote_actions.append(action)
    self.resolve_actions(vote_actions, game=game)

    # Count votes
    for player in game.players:
      if votes[player] and votes[player].alive:
        game.log.append(events.VotedFor(player, votes[player], votes=player.votes, original_vote=self.votes[player]))
        candidates[votes[player]] += player.votes

    # Try to lynch the first viable candidate by number of votes or coin flip
    candidate_list = game.shuffled([(c,p) for p,c in sorted(candidates.items())])
    candidate_list = [p for c,p in sorted(candidate_list, reverse=True)]
    victim = candidate_list[0] if len(candidate_list) > 0 else None
    if victim:
      victim.on_lynched(game=game, player=victim)
    else:
      game.log.append(events.NoLynch())

    # Advance effects
    for player in game.all_players:
      for effect in player.effects:
        effect.expiration.advance_day()
