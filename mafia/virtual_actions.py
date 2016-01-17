from .actions import *

class VirtualAction(object):
  def __init__(self, action):
    super().__init__()
    self.action = action

class FactionAction(VirtualAction):
  def __init__(self, faction, action):
    super().__init__(action)
    self.faction = faction
