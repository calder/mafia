import itertools
import sys

def return_none(): return None
def return_0(): return 0

def assert_equal(x, y):
  if x != y:
    print("------------------------------------------------------------")
    print(x)
    print("-----------------------------!=-----------------------------")
    print(y)
    print("------------------------------------------------------------")
  assert x == y

def assert_contains(element, list):
  if element not in list:
    print("------------------------------------------------------------")
    print(element)
    print("---------------------------not in---------------------------")
    print(list)
    print("------------------------------------------------------------")
  assert element in list

class SingletonValue(object):
  def __init__(self, name, id):
    self.name = name
    self.id   = id

  def __repr__(self):
    return self.name

  def __eq__(self, other):
    return isinstance(other, SingletonValue) and self.id == other.id

def flatten(list_of_lists):
  return list(itertools.chain(*list_of_lists))

def str_list(list, empty):
  if len(list) == 0: return empty
  if len(list) == 1: return str(list[0])
  return ", ".join([str(e) for e in list[:-1]]) + " and " + str(list[-1])

def str_player_list(list): return str_list(list, "nobody")

def has_method(object, method):
  return callable(getattr(object, method, None))

def matches(x, y, *, debug=False, **kwargs):
  if type(x) != type(y):
    if debug: print("Types don't match:\n  %r\n  %r" % (type(x), type(y)))
    return False
  xkeys = x.__dict__.keys()
  ykeys = y.__dict__.keys()
  if xkeys != ykeys:
    if debug: print("Keys don't match:\n  %r\n  %r" % (xkeys, ykeys))
    return False
  for k, xv, yv in [(k, x.__dict__[k], y.__dict__[k]) for k in xkeys]:
    if has_method(xv, "matches"):
      if not xv.matches(yv, **kwargs):
        if debug: print("Field %r doesn't match:\n  %r\n  %r" % (k, xv, yv))
        return False
    else:
      if xv != yv:
        if debug: print("Field %r not equal:\n  %r\n  %r" % (k, xv, yv))
        return False
  return True

def fill_randomly(x, **kwargs):
  for k, v in x.__dict__.items():
    if has_method(v, "random_instance"):
      x.__dict__[k] = v.random_instance(**kwargs)

def strict_subclasses(cls, namespace):
  """Return all strict subclasses of the given type in a namespace."""
  return [c for c in vars(namespace).values()
                  if type(c) == type
                  and issubclass(c, cls)
                  and c != cls]
