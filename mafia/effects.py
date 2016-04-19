import re

from .action_helpers import *
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
  def __str__(self):
    return "Days(%d)" % self.days
  def expired(self):     return self.days <= 0
  def advance_day(self): self.days -= 1

class Manual(Expiration):
  """A manually set expiration."""
  def __init__(self):
    self._expired = False
  def set_expired(self, expired):
    self._expired = expired
  def expired(self):
    return self._expired

class Nights(Expiration):
  """Expires after number of nights. Unaffected by intervening days."""
  def __init__(self, nights):
    self.nights = nights
  def __str__(self):
    return "Nights(%d)" % self.nights
  def expired(self):       return self.nights <= 0
  def advance_night(self): self.nights -= 1

class Never(Expiration):
  """Never expires."""
  def __str__(self):
    return "Never()"
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
  @property
  def blocked(self):
    return True

class ChangeRole(Effect):
  def __init__(self, role, *, expiration=Never(), **kwargs):
    super().__init__(expiration=expiration, **kwargs)
    self._role = role

  @property
  def role(self):
    return self._role

class Dead(Effect):
  def __init__(self, *, expiration=Never(), **kwargs):
    super().__init__(expiration=expiration, **kwargs)

  @property
  def alive(self):
    return False

class Delayed(Effect):
  @property
  def delayed(self):
    return True

class ExtraAction(Effect):
  def __init__(self, extra_actions=1, *, expiration=Nights(2), **kwargs):
    super().__init__(expiration=expiration, **kwargs)
    self.extra_actions = extra_actions

  def action_count_fn(self, base):
    return self.extra_actions + base()

class GuardedBy(Effect):
  def __init__(self, bodyguard, *, elite=False, **kwargs):
    super().__init__(**kwargs)
    self.bodyguard = bodyguard
    self.elite     = elite

  def on_killed_fn(self, base, *, game, player, by, **kwargs):
    game.log.append(events.Protected(player))
    resolve_kill(by, self.bodyguard, game=game, **kwargs)
    if self.elite: resolve_kill(self.bodyguard, by, game=game)

class Unlynchable(Effect):
  def on_lynched_fn(self, base, *, game, player):
    game.log.append(events.NoLynch())

class MustTarget(Effect):
  def __init__(self, must_target, **kwargs):
    super().__init__(**kwargs)
    self.must_target = must_target

class Protected(Effect):
  def on_killed_fn(self, base, *, game, player, by, protectable, **kwargs):
    if protectable: game.log.append(events.Protected(player))
    else:           return base()

class Stoned(Effect):
  def __init__(self, **kwargs):
    super().__init__(expiration=Manual(), **kwargs)

  def on_killed_fn(self, base, *, game, player, by, protectable, **kwargs):
    if protectable:
      game.log.append(events.Protected(player))
      self.expiration.set_expired(True)
    else:
      return base()

class SwitchedWith(Effect):
  def __init__(self, switched_with, **kwargs):
    super().__init__(**kwargs)
    self.switched_with = switched_with

class VotesWith(Effect):
  def __init__(self, votes_with, **kwargs):
    super().__init__(**kwargs)
    self.votes_with = votes_with
