def assert_equal(x, y):
  if x != y:
    print("--------------------1--------------------")
    print(x)
    print("--------------------2--------------------")
    print(y)
    print("-----------------------------------------")
  assert x == y

def assert_one_of(x, *ys):
  if x not in ys:
    print("--------------------1--------------------")
    print(x)
    print("-----------------------------------------")
  assert x in ys

def assert_matches(x, y):
  if not x.matches(y):
    print("--------------------1--------------------")
    print(x)
    print("--------------------2--------------------")
    print(y)
    print("-----------------------------------------")
  assert x.matches(y)

class SingletonValue(object):
  pass

class identitydefaultdict(dict):
  def __getitem__(self, key):
    if key in self:
      return super().__getitem__(key)
    else:
      return key

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
