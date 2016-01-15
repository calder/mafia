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
    return "\n".join([str(event) for event in self])

  def phase(self, phase):
    return Log(filter(lambda event: event.phase == phase, self))
