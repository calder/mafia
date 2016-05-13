class InvalidAction(Exception):
  pass

class IllegalAction(InvalidAction):
  pass

class InvalidPlayer(InvalidAction):
  def __init__(self, player):
    self.player = player

  def __str__(self):
    return "%r is not a valid player." % self.player

class InvalidSender(InvalidAction):
  def __str__(self):
    return "You are not allowed to submit that action."

class MalformedAction(InvalidAction):
  def __init__(self, help):
    self.help = help

  def __str__(self):
    help = "\n  ".join(self.help)
    return "Action must be one of the following:\n  %s" % help

class MalformedVote(InvalidAction):
  def __str__(self):
    return "Votes must take the form:\n  vote for PLAYER"

class NoFactionAction(InvalidAction):
  def __str__(self):
    return "No faction actions available."

class NoIndividualAction(InvalidAction):
  def __str__(self):
    return "No actions available."
