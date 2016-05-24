class InvalidAction(Exception):
  def __str__(self):
    return "Invalid action."

class IllegalAction(InvalidAction):
  def __str__(self):
    return "Illegal action."

class InvalidPlayer(InvalidAction):
  def __init__(self, player):
    self.player = player

  def __str__(self):
    return "%r is not a valid player." % self.player

class WrongPhase(InvalidAction):
  def __init__(self, *, right_phase):
    self.right_phase = right_phase

  def __str__(self):
    return "That action can only be used during the %s." % \
           self.right_phase.__class__.__name__
