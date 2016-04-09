from functools import wraps

def mixin(mixin_attr):
  def inner(f):
    @property
    @wraps(f)
    def wrapper(self):
      for mixin in reversed(getattr(self, mixin_attr)):
        if hasattr(mixin, f.__name__):
          return getattr(mixin, f.__name__)
      return f(self)
    return wrapper
  return inner
