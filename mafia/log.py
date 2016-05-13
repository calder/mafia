from . import events
from .util import *

from collections import *
from enum import *

class Log(list):
  def __init__(self, list=None, *, phase=None):
    if list: super().__init__(list)
    if phase:
      for event in self:
        event.phase = phase
    self.append_callbacks = []
    self.current_phase = None

  def __str__(self):
    return "\n".join([event.colored_str() for event in self])

  def __add__(self, other):
    return Log(super().__add__(other))

  def append(self, event):
    event.phase = self.current_phase
    for f in self.append_callbacks: f(event)
    super().append(event)

  def on_append(self, callback):
    self.append_callbacks.append(callback)

  def filter(self, predicate):
    return Log(filter(predicate, self))

  def phase(self, phase):
    return self.filter(lambda event: event.phase == phase)

  def this_phase(self):
    return self.phase(self.current_phase)

  def type(self, type):
    return self.filter(lambda event: isinstance(event, type))

  def has_been_lynched(self, player):
    return len(self.type(events.Lynched).filter(lambda lynch: lynch.player == player)) > 0

  def visits_by(self, player, *, include_invisible=False):
    def include(visit):
      return visit.player == player and (visit.visible or include_invisible)
    return self.type(events.Visited).filter(include)

  def visits_to(self, player, *, include_invisible=False):
    def include(visit):
      return visit.target == player and (visit.visible or include_invisible)
    return self.type(events.Visited).filter(include)
