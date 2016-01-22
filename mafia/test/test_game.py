from mafia import Game

class TestGame(Game):
  def __init__(self):
    super().__init__(42)
    self.log.on_append(self.print_event)

  def print_event(self, event):
    print(event.colored_str())
