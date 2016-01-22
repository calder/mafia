class PhaseState(object):
  """The transient state of a phase as it's being resolved."""

  def __init__(self, phase, game):
    self.phase = phase
    self.game  = game

  def log(self, event):
    event.phase = self.phase
    self.game.log.append(event)
