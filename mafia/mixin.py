"""
Mixins are objects that can be "attached" to other objects to override their
functions or properties. This is used by effects to temporarily modify Player
and Role objects.

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

def mixin_fn(mixin_attr):
  def decorator(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
      def call_next():
        for mixin in reversed(getattr(self, mixin_attr)):
          # Look for the function variant first
          if hasattr(mixin, f.__name__ + "_fn"):
            def call(mixin):
              mixin_f = getattr(mixin, f.__name__ + "_fn")
              value = mixin_f(lambda: next(next_gen)(), *args, **kwargs)
              return value
            yield lambda mixin=mixin: call(mixin)

          # Look for the attribute variant second
          if hasattr(mixin, f.__name__):
            def call(mixin):
              value = getattr(mixin, f.__name__)
              return value
            yield lambda mixin=mixin: call(mixin)

        # Fall back to the base implementation
        yield lambda: f(self, *args, **kwargs)

      next_gen = call_next()
      return next(next_gen)()

    return wrapper

  return decorator

def mixin(mixin_attr):
  return lambda f: property(mixin_fn(mixin_attr)(f))
