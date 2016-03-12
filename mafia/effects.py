from .day import *
from .night import *

class Expiration(object):
  def __init__(self, *, days=0, nights=0):
    self.days   = days
    self.nights = nights

  def advance(self, phase):
    if   isinstance(phase, Day):   self.days   -= 1
    elif isinstance(phase, Night): self.nights -= 1
    else: assert False, "Unhandled Phase type: %s" % type(phase)

  def passed(self):
    return self.days <= 0 and self.nights <= 0

def Days(days): return Expiration(days=days)
def Nights(nights): return Expiration(nights=nights)

class Effect(object):
  """Effects are temporary alterations which can be applied to players."""

  def __init__(self, *, expiration=None):
    self.expiration = expiration or Days(1)

  @property
  def expired(self):
    return self.expiration.passed()

class Blocked(Effect):
  blocked = True

class ExtraAction(Effect):
  def __init__(self, extra_actions=1, expiration=Nights(2), **kwargs):
    super().__init__(expiration=expiration, **kwargs)
    self.extra_actions = extra_actions

class Delayed(Effect):
  delayed = True

class MustTarget(Effect):
  def __init__(self, must_target, **kwargs):
    super().__init__(**kwargs)
    self.must_target = must_target

class Protected(Effect):
  bulletproof = True

class SwitchedWith(Effect):
  def __init__(self, target, **kwargs):
    super().__init__(**kwargs)
    self.switched_with = target

class VotesWith(Effect):
  def __init__(self, votes_with, **kwargs):
    super().__init__(**kwargs)
    self.votes_with = votes_with
