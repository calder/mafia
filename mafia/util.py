def assert_equal(x, y):
  if x != y:
    print("--------------------1--------------------")
    print(x)
    print("--------------------2--------------------")
    print(y)
    print("-----------------------------------------")
  assert x == y

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

def all_fields_match(x, y, **kwargs):
  if type(x) != type(y):
    return False
  keys = x.__dict__.keys()
  if y.__dict__.keys() != keys:
    return False
  for xv, yv in [(x.__dict__[k], y.__dict__[k]) for k in keys]:
    if has_method(xv, "matches"):
      if not xv.matches(yv, **kwargs):
        return False
    else:
      if xv != yv:
        return False
  return True

def fill_randomly(x, **kwargs):
  keys = x.__dict__.keys()
  if y.__dict__.keys() != keys:
    return False
  for k, v in x.__dict__.items():
    if has_method(v, "fill_randomly"):
      x.__dict__[k] = v.fill_randomly(**kwargs)
