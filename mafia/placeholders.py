class Placeholder(object):
  class Placeholder(object):
    pass

  class Self(Placeholder):
    pass

  class Player(Placeholder):
    pass

  class FactionMember(Placeholder):
    def __init__(self, faction):
      self.faction = faction

  class PlayerExcept(Placeholder):
    def __init__(self, exclude):
      self.exclude = exclude
