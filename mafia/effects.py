from .day import *
from .night import *
from .util import *

class Expiration(object):
  def __init__(self, *, days=0, nights=0):
    self.days   = days
    self.nights = nights

  def __str__(self):
    return "days=%d, nights=%d" % (self.days, self.nights)

  def expired(self):
    return self.days <= 0 and self.nights <= 0

def Days(days): return Expiration(days=days)
def Nights(nights): return Expiration(nights=nights)

class Effect(object):
  """Effects are temporary alterations which can be applied to players."""

  def __init__(self, *, expiration=None):
    self.expiration = expiration or Days(1)

  def __str__(self):
    return "%s(expiration=%s)" % (self.__class__.__name__, str(self.expiration))

  @property
  def expired(self):
    return self.expiration.expired()

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
  def __init__(self, bodyguard, **kwargs):
    super().__init__(**kwargs)
    self.guarded_by = bodyguard

class Unlynchable(Effect):
  lynchable = False

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
