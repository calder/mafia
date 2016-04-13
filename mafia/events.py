from .alignment import *
from .util import *

from termcolor import colored

PUBLIC = SingletonValue("PUBLIC")

class Event(object):
  def __init__(self, *, phase=None, to=None):
    self.phase = phase  # Filled in by Log.append
    self.to    = to     # None, a player, a faction, or PUBLIC

  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

  def __str__(self):
    if self.to is None:
      return "%s: [%s]" % (self.phase, self._str())
    elif self.to is PUBLIC:
      return "%s: %s" % (self.phase, self._str())
    else:
      to = self.to if not isinstance(self.to, list) else \
           ", ".join([str(p) for p in self.to])
      return "%s: %s: %s" % (self.phase, to, self._str())

  @property
  def color(self):
    if self.to is not None: return "cyan"

  @property
  def style(self):
    if self.to is PUBLIC: return ["bold"]

  def colored_str(self):
    return colored(str(self), self.color, attrs=self.style)

class Announcement(Event):
  pass

class Result(Event):
  def __init__(self, *, target, to):
    super().__init__(to=to)
    self.target = target

#########################
###   Announcements   ###
#########################

class FactionAnnouncement(Event):
  def __init__(self, faction, members):
    super().__init__(to=members)
    self.faction = faction
    self.members = members

  def _str(self):
    return "You are the %s." % self.faction.name

class RoleAnnouncement(Event):
  def __init__(self, player, role):
    super().__init__(to=player)
    self.player = player
    self.role   = role

  def _str(self):
    return "You are the %s." % self.player.role

##################
###   Events   ###
##################

class Blocked(Event):
  color = "yellow"

  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was blocked." % self.player

class Busdriven(Event):
  color = "yellow"

  def __init__(self, player1, player2):
    super().__init__()
    self.player1 = player1
    self.player2 = player2

  def _str(self):
    return "%s was busdriven with %s." % (self.player1, self.player2)

class Delayed(Event):
  color = "yellow"

  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s's action was delayed." % self.player

class Died(Event):
  color = "red"

  def __init__(self, player):
    super().__init__()
    self.player = player
    self.to     = PUBLIC

  def _str(self):
    return "%s, the %s, has died." % (self.player, self.player.role)

class Doubled(Event):
  color = "green"

  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s's action was doubled." % self.player

class Lynched(Died):
  def _str(self):
    return "%s, the %s, was lynched." % (self.player, self.player.role)

class NoLynch(Event):
  def _str(self):
    return "Nobody was lynched."

class Protected(Event):
  color = "green"

  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was protected." % self.player

class Visited(Event):
  def __init__(self, player, target, *, visible=True, original_target=None):
    super().__init__()
    self.player          = player
    self.target          = target
    self.visible         = visible
    self.original_target = original_target or self.target

  def _str(self):
    visited = "visited" if self.visible else "secretly visited"
    target = self.target if self.target == self.original_target else \
             "%s (busdriven from %s)" % (self.target, self.original_target)
    return "%s %s %s." % (self.player, visited, target)

class VotedFor(Event):
  def __init__(self, player, vote, *, votes=1, original_vote=None):
    super().__init__()
    self.player        = player
    self.vote          = vote
    self.votes         = votes
    self.original_vote = original_vote or self.vote

  def _str(self):
    votes = "" if self.votes == 1 else " with %d votes" % self.votes
    vote = self.vote if self.vote == self.original_vote else \
           "%s (politicianed from %s)" % (self.vote, self.original_vote)
    return "%s voted for %s%s." % (self.player, vote, votes)

###################
###   Results   ###
###################

class VisiteesResult(Result):
  def __init__(self, visitees, *, target, to):
    super().__init__(target=target, to=to)
    self.visitees = visitees

  def _str(self):
    return "%s visited %s." % (self.target, str_player_list(self.visitees))

class VisitorsResult(Result):
  def __init__(self, visitors, *, target, to):
    super().__init__(target=target, to=to)
    self.visitors = visitors

  def _str(self):
    return "%s visited %s." % (str_player_list(self.visitors), self.target)

class InvestigationResult(Result):
  def __init__(self, alignment, *, target, to):
    super().__init__(target=target, to=to)
    self.alignment = "good" if alignment == Alignment.good else "evil"

  def _str(self):
    return "%s is %s." % (self.target, self.alignment)
