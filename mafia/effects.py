import re

from .day import *
from .night import *
from .util import *

class Expiration(object):
  """An expiration condition for an Effect."""
  def expired(self):       raise NotImplementedError()
  def advance_day(self):   pass
  def advance_night(self): pass
  def on_used(self):       pass

class Days(Expiration):
  """Expires after a number of days. Unaffected by intervening nights."""
  def __init__(self, days):
    self.days = days
  def expired(self):       return self.days <= 0
  def advance_day(self):   self.days -= 1

class Nights(Expiration):
  """Expires after number of nights. Unaffected by intervening days."""
  def __init__(self, nights):
    self.nights = nights
  def expired(self):       return self.nights <= 0
  def advance_night(self): self.nights -= 1

class Never(Expiration):
  """Never expires."""
  def expired(self): return False

class Effect(object):
  """Temporary alterations which can be applied to players or roles."""

  def __init__(self, *, expiration=None):
    self.expiration = expiration or Days(1)

  def __str__(self):
    return "%s(expiration=%s)" % (self.__class__.__name__, str(self.expiration))

  def __getattribute__(self, attr):
    special = re.compile(r"__.*__|expiration")
    if special.match(attr):
      return super().__getattribute__(attr)

    if self.expiration.expired():
      raise AttributeError()

    return super().__getattribute__(attr)

class Blocked(Effect):
  blocked = True

class ExtraAction(Effect):
  def __init__(self, extra_actions=1, *, expiration=Nights(2), **kwargs):
    super().__init__(expiration=expiration, **kwargs)
    self.extra_actions = extra_actions

  def action_count_fn(self, next):
    return self.extra_actions + next()

class Delayed(Effect):
  delayed = True

class GuardedBy(Effect):
  def __init__(self, bodyguard, *, elite=False, **kwargs):
    super().__init__(**kwargs)
    self.guarded_by    = bodyguard
    self.elite_guarded = elite

class Unlynchable(Effect):
  unlynchable = True

class MustTarget(Effect):
  def __init__(self, must_target, **kwargs):
    super().__init__(**kwargs)
    self.must_target = must_target

class Protected(Effect):
  bulletproof = True

class SwitchedWith(Effect):
  def __init__(self, switched_with, **kwargs):
    super().__init__(**kwargs)
    self.switched_with = switched_with

class VotesWith(Effect):
  def __init__(self, votes_with, **kwargs):
    super().__init__(**kwargs)
    self.votes_with = votes_with
