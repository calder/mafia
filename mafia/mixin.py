from functools import wraps

def mixin(mixin_attr):
  def inner(f):
    @property
    @wraps(f)
    def wrapper(self):
      name = f.__name__
      for mixin in getattr(self, mixin_attr):
        if hasattr(mixin, name):
          return getattr(mixin, name)
      return f(self)
    return wrapper
  return inner
