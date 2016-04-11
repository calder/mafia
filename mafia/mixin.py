"""
Mixins are objects that can be "attached" to other objects to override their
functions or properties. This is used by effects to temporarily modify players.

Usage:
  class Base(object):
    def __init__(self):
      self.mixins = []

    @mixin("mixins")
    def foo(self): return 123

  class Mixin(object):
    def __init__(self, value):
      self.foo = value

  base = Base()
  assert(base.foo == 123)
  base.mixins.append(Mixin(456))
  assert(base.foo == 456)
"""

from functools import wraps

def mixin_func(mixin_attr):
  def decorator(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
      def call_next():
        for mixin in reversed(getattr(self, mixin_attr)):
          # Look for the function variant first
          if hasattr(mixin, f.__name__ + "_fn"):
            mixin_f = getattr(mixin, f.__name__ + "_fn")
            yield lambda: mixin_f(next(next_gen), *args, **kwargs)

          # Look for the attribute variant second
          if hasattr(mixin, f.__name__):
            yield lambda: getattr(mixin, f.__name__)

        # Fall back to the base implementation
        yield lambda: f(self, *args, **kwargs)

      next_gen = call_next()
      return next(next_gen)()

    return wrapper

  return decorator

def mixin(mixin_attr):
  def decorator(f):
    @property
    @wraps(f)
    def wrapper(self):
      def call_next():
        for mixin in reversed(getattr(self, mixin_attr)):
          # Look for the function variant first
          if hasattr(mixin, f.__name__ + "_fn"):
            mixin_f = getattr(mixin, f.__name__ + "_fn")
            yield lambda: mixin_f(next(next_gen))

          # Look for the attribute variant second
          if hasattr(mixin, f.__name__):
            yield lambda: getattr(mixin, f.__name__)

        # Fall back to the base implementation
        yield lambda: f(self)

      next_gen = call_next()
      return next(next_gen)()

    return wrapper

  return decorator
