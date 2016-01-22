from .util import *

import copy

class TargetList(list):
  def matches(self, other, **kwargs):
    return len(self) == len(other) and \
           all([s.matches(o, **kwargs) for s, o in zip(self, other)])

  def random_instance(self, **kwargs):
    return TargetList([t.random_instance(**kwargs) for t in self])

class ActionBase(object):
  compelled = False

  def concrete_action(self):
    raise NotImplementedError()

  def matches(self, other, **kwargs):
    return matches(self, other, **kwargs)

  def with_player(self, player):
    clone = copy.copy(self)
    clone.player = player
    return clone

  def random_instance(self, **kwargs):
    clone = copy.copy(self)
    fill_randomly(clone, **kwargs)
    return clone
