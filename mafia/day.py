from . import effects
from . import events
from .log import *
from .phase import *
from .util import *

from collections import *
import copy

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
    self.number = number
    self.votes  = defaultdict(lambda: None)

  def __str__(self):
    return "Day %d" % self.number

  def set_vote(self, player, candidate):
    self.votes[player] = candidate

  def _resolve(self, game):
    votes      = defaultdict(lambda: None)
    candidates = defaultdict(lambda: 0)

    # Determine actual votes after politicianing
    for player in game.players:
      if player.votes_with.alive:
        votes[player] = self.votes[player.votes_with]

    # Apply vote actions
    for player in game.players:
      if votes[player] and player.vote_action:
        action = player.vote_action.with_target(votes[player])
        if player.vote_action.matches(action): action.resolve(game)

    # Count votes
    for player in sorted(game.players):
      if votes[player]:
        game.log.append(events.VotedFor(player, votes[player], votes=player.votes, original_vote=self.votes[player]))
        candidates[votes[player]] += player.votes

    # Lynch the first viable candidate by number of votes, then coin flip
    candidate_list = game.shuffled([(c,p) for p,c in candidates.items()])
    ranked_candidates = [p for c,p in sorted(candidate_list, reverse=True)]
    for candidate in ranked_candidates:
      if candidate and candidate.alive and candidate.lynchable:
        game.log.append(events.Lynched(candidate))
        candidate.alive = False
        return
    game.log.append(events.NoLynch())
