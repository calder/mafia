
class Player(object):
  def __init__(self, name, role):
    self.name = name
    self.role = role
    self.alive = True

  def __str__(self):
    return self.name

  def __lt__(self, other):
    return self.name < other.name

  @property
  def faction(self):
      return self.role.faction

  @property
  def alignment(self):
      return self.role.alignment

  @property
  def votes(self):
      return self.role.votes


  def matches(self, other, **kwargs):
    return self == other
