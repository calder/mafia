from .log import *
from .phase import *
from .util import *

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
    self.votes  = {}

  def __str__(self):
    return "Day %d" % self.number

  def set_vote(self, player, candidate):
    self.votes[player] = candidate

  def _resolve(self, game):
    candidates = defaultdict(lambda: 0)

    for player, vote in self.votes.items():
      candidates[vote] += player.votes

    candidate_list = game.shuffled([(c,p) for p,c in candidates.items()])
    ranked_candidates = [p for c,p in sorted(candidate_list, reverse=True)]
    for candidate in ranked_candidates:
      game.log.append(Lynched(candidate))
      candidate.alive = False
      return
