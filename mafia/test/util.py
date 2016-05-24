from mafia import Game

class LoggingGame(Game):
  """A Game subclass that automatically logs all events."""

  def __init__(self):
    super().__init__(seed=42)
    self.log.on_append(self.print_event)

  def print_event(self, event):
    print(event.colored_str())
