class SingletonValue(object):
  pass

class identitydefaultdict(dict):
  def __getitem__(self, key):
    if key in self:
      return super().__getitem__(key)
    else:
      return key

d = identitydefaultdict()
assert d[123] == 123
d[123] = 456
assert d[123] == 456
