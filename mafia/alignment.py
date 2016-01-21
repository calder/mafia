import enum

class Alignment(enum.Enum):
  good    = 1
  neutral = 2
  evil    = 3

  def __str__(self):
    return self.name
