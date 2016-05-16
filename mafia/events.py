from .alignment import *
from .player import *
from .util import *

from termcolor import colored

PUBLIC = SingletonValue("PUBLIC", 462028731)
START = SingletonValue("Start", 502402573)

class Event(object):
  def __init__(self, *, phase=None, to=None):
    if isinstance(to, Player):
      to = [to]

    self.phase = phase  # Filled in by Log.append
    self.to    = to     # None, a list of players, or PUBLIC

  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

  def __str__(self):
    if not self.to:
      return "%s: [%s]" % (self.phase, self.message)
    elif self.to == PUBLIC:
      return "%s: %s" % (self.phase, self.message)
    else:
      to = self.to if not isinstance(self.to, list) else \
           ", ".join([str(p) for p in self.to])
      return "%s: %s: %s" % (self.phase, to, self.message)

  @property
  def full_message(self):
    return self.message

  @property
  def color(self):
    if self.to != None: return "cyan"

  @property
  def style(self):
    if self.to == PUBLIC: return ["bold"]

  def colored_str(self):
    return colored(str(self), self.color, attrs=self.style)

class Announcement(Event):
  pass

class PublicEvent(Event):
  def __init__(self, **kwargs):
    super().__init__(to=PUBLIC, **kwargs)

class Result(Event):
  def __init__(self, *, target, to, **kwargs):
    super().__init__(to=to, **kwargs)
    self.target = target

#########################
###   Announcements   ###
#########################

class FactionAnnouncement(Event):
  def __init__(self, faction, members, **kwargs):
    super().__init__(to=members, **kwargs)
    self.faction = faction
    self.members = members

  @property
  def message(self):
    return "You are the %s." % self.faction.name

  @property
  def full_message(self):
    return "%s, you are the %s." % (str_player_list(self.faction.members), self.faction.name)

class FactionLeaderAnnouncement(Event):
  def __init__(self, faction, leader, **kwargs):
    super().__init__(to=leader, **kwargs)
    self.faction = faction
    self.leader  = leader

  @property
  def message(self):
    if self.phase == START:
      return "You are the leader of the %s." % self.faction
    else:
      return "You are now the leader of the %s." % self.faction

  @property
  def full_message(self):
    parts = [self.message]
    if self.faction.action:
      commands = "\n".join(["  " + i for i in self.faction.action.help()])
      parts.append("---------------------------------------\n" \
                   "You may send me the following commands:\n%s" % commands)
    return "\n\n".join(parts)

class RoleAnnouncement(Event):
  def __init__(self, player, role, **kwargs):
    super().__init__(to=player, **kwargs)
    self.player = player
    self.role   = role

  @property
  def message(self):
    if self.phase == START:
      return "You are the %s." % self.player.role
    else:
      return "You are now the %s." % self.player.role

  @property
  def full_message(self):
    parts = [self.message]
    parts += self.role.descriptions
    parts += [self.role.objective]
    if self.player.action:
      commands = self.player.action.help() + ["vote for PLAYER", "unvote"]
      commands = "\n".join(["  " + c for c in commands])
      parts.append("---------------------------------------\n" \
                   "You may send me the following commands:\n%s" % commands)
    return "\n\n".join(parts)

##################
###   Events   ###
##################

class Blocked(Event):
  color = "yellow"

  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.player = player

  @property
  def message(self):
    return "%s was blocked." % self.player

class Busdriven(Event):
  color = "yellow"

  def __init__(self, player1, player2, **kwargs):
    super().__init__(**kwargs)
    self.player1 = player1
    self.player2 = player2

  @property
  def message(self):
    return "%s was busdriven with %s." % (self.player1, self.player2)

class Delayed(Event):
  color = "yellow"

  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.player = player

  @property
  def message(self):
    return "%s's action was delayed." % self.player

class Died(PublicEvent):
  color = "red"

  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.player = player

  @property
  def message(self):
    return "%s, the %s, has died." % (self.player, self.player.role)

class Doubled(Event):
  color = "green"

  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.player = player

  @property
  def message(self):
    return "%s's action was doubled." % self.player

class Lynched(Died):
  @property
  def message(self):
    return "%s, the %s, was lynched." % (self.player, self.player.role)

class NoDeaths(PublicEvent):
  color = "green"

  @property
  def message(self):
    return "Nobody died."

class NoLynch(PublicEvent):
  color = "green"

  @property
  def message(self):
    return "Nobody was lynched."

class Protected(Event):
  color = "green"

  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.player = player

  @property
  def message(self):
    return "%s was protected." % self.player

class Visited(Event):
  def __init__(self, player, target, *, visible=True, original_target=None, **kwargs):
    super().__init__(**kwargs)
    self.player          = player
    self.target          = target
    self.visible         = visible
    self.original_target = original_target or self.target

  @property
  def message(self):
    visited = "visited" if self.visible else "secretly visited"
    target = self.target if self.target == self.original_target else \
             "%s (busdriven from %s)" % (self.target, self.original_target)
    return "%s %s %s." % (self.player, visited, target)

class VotedFor(Event):
  def __init__(self, player, vote, *, votes=1, original_vote=None, **kwargs):
    super().__init__(**kwargs)
    self.player        = player
    self.vote          = vote
    self.votes         = votes
    self.original_vote = original_vote or self.vote

  @property
  def message(self):
    votes = "" if self.votes == 1 else " with %d votes" % self.votes
    vote = self.vote if self.vote == self.original_vote else \
           "%s (politicianed from %s)" % (self.vote, self.original_vote)
    return "%s voted for %s%s." % (self.player, vote, votes)

###################
###   Results   ###
###################

class VisiteesResult(Result):
  def __init__(self, visitees, *, target, to, **kwargs):
    super().__init__(target=target, to=to, **kwargs)
    self.visitees = visitees

  @property
  def message(self):
    return "%s visited %s." % (self.target, str_player_list(self.visitees))

class VisitorsResult(Result):
  def __init__(self, visitors, *, target, to, **kwargs):
    super().__init__(target=target, to=to, **kwargs)
    self.visitors = visitors

  @property
  def message(self):
    return "%s visited %s." % (str_player_list(self.visitors), self.target)

class InvestigationResult(Result):
  def __init__(self, alignment, *, target, to, **kwargs):
    super().__init__(target=target, to=to, **kwargs)
    self.alignment = "good" if alignment == Alignment.good else "evil"

  @property
  def message(self):
    return "%s is %s." % (self.target, self.alignment)
