from .util import *

from termcolor import colored

PUBLIC = SingletonValue()

class Event(object):
  def __init__(self, *, to=None):
    self.phase  = None  # Filled in by State.log
    self.to     = to    # None, a player, a faction, or PUBLIC

  def __eq__(self, other):
    return type(self) == type(other) and self.__dict__ == other.__dict__

  def __str__(self):
    if self.to is None:
      return "%s: [%s]" % (self.phase, self._str())
    elif self.to is PUBLIC:
      return "%s: %s" % (self.phase, self._str())
    else:
      return "%s: %s: %s" % (self.phase, self.to, self._str())

  @property
  def color(self):
    if self.to is not None: return "cyan"

  @property
  def style(self):
    if self.to is PUBLIC: return ["bold"]

  def colored_str(self):
    return colored(str(self), self.color, attrs=self.style)

class Visited(Event):
  def __init__(self, player, target, *, visible=True):
    super().__init__()
    self.player  = player
    self.target  = target
    self.visible = visible

  def _str(self):
    visited = "visited" if self.visible else "secretly visited"
    return "%s %s %s." % (self.player, visited, self.target)

class Blocked(Event):
  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was blocked." % self.player

class Saved(Event):
  def __init__(self, player):
    super().__init__()
    self.player = player

  def _str(self):
    return "%s was saved." % self.player

class Died(Event):
  color = "red"

  def __init__(self, player):
    super().__init__()
    self.player = player
    self.to     = PUBLIC

  def _str(self):
    return "%s, the %s, has died." % (self.player, self.player.role)


class TurntUp(Event):
  def __init__(self, player, alignment, *, to):
    super().__init__(to=to)
    self.player    = player
    self.alignment = alignment

  def _str(self):
    return "%s is %s." % (self.player, self.alignment)

class SawVisit(Event):
  def __init__(self, player, *, to):
    super().__init__(to=to)
    self.player = player

  def _str(self):
    return "Your target visited %s." % self.player

class SawVisitor(Event):
  def __init__(self, player, *, to):
    super().__init__(to=to)
    self.player = player

  def _str(self):
    return "%s visited your target." % self.player
