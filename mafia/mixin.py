from functools import wraps

def mixin(mixins):
  def inner(prop):
    @property
    @wraps(prop)
    def wrapper(self):
      name = prop.__name__
      for mixin in getattr(self, mixins):
        if hasattr(mixin, name):
          return getattr(mixin, name)
      return prop(self)
    return wrapper
  return inner

def sum_present(mixins, prop):
  return sum([getattr(m, prop, 0) for m in mixins])
