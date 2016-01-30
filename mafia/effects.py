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

class Days(Expiration):
  def __init__(self, days):
    super().__init__(days=days)

class Nights(Expiration):
  def __init__(self, nights):
    super().__init__(nights=nights)

class Effect(object):
  """Effects are temporary alterations which can be applied to players."""

  def __init__(self, *, expiration=None):
    self.expiration = expiration or Days(1)

  @property
  def expired(self):
    return self.expiration.passed()

class Blocked(Effect):
  blocked = True

class MustTarget(Effect):
  def __init__(self, player, **kwargs):
    super().__init__(**kwargs)
    self.must_target = player

class Protected(Effect):
  protected = True

class VotesWith(Effect):
  def __init__(self, votes_with, **kwargs):
    super().__init__(**kwargs)
    self.votes_with = votes_with

class SwitchedWith(Effect):
  def __init__(self, target, **kwargs):
    super().__init__(**kwargs)
    self.switched_with = target
