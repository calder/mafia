from .events import *
from .util import *

from collections import *
from enum import *

class Log(list):
  def __init__(self, list=None, *, phase=None):
    if list: super().__init__(list)
    if phase is not None:
      for event in self:
        event.phase = phase

  def __str__(self):
    return "\n".join([event.colored_str() for event in self])

  def filter(self, predicate):
    return Log(filter(predicate, self))

  def phase(self, phase):
    return self.filter(lambda event: event.phase == phase)

  def type(self, type):
    return self.filter(lambda event: isinstance(event, type))

  def visits_by(self, player, *, include_invisible=False):
    def include(visit):
      return visit.player == player and (visit.visible or include_invisible)
    return self.type(Visited).filter(include)

  def visits_to(self, player, *, include_invisible=False):
    def include(visit):
      return visit.target == player and (visit.visible or include_invisible)
    return self.type(Visited).filter(include)

_test_log = Log([
  Visited("Alice", "Bob"),
  Visited("Bob", "Alice"),
  Visited("Eve", "Alice"),
  Visited("Eve", "Bob", visible=False),
])

assert_equal(_test_log.visits_to("Bob"), Log([
  Visited("Alice", "Bob"),
]))

assert_equal(_test_log.visits_to("Bob", include_invisible=True), Log([
  Visited("Alice", "Bob"),
  Visited("Eve", "Bob", visible=False),
]))

assert_equal(_test_log.visits_by("Eve"), Log([
  Visited("Eve", "Alice"),
]))

assert_equal(_test_log.visits_by("Eve", include_invisible=True), Log([
  Visited("Eve", "Alice"),
  Visited("Eve", "Bob", visible=False),
]))
