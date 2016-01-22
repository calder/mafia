from .action_base import *
from .effects import *
from .events import *
from .log import *
from .placeholders import *
from .util import *

class Action(ActionBase):
  protectable = False

  def __init__(self, player, targets, **kwargs):
    if not isinstance(targets, list):
      targets = TargetList([targets])

    self.player      = player
    self.raw_targets = TargetList(targets)
    self.targets     = TargetList(targets)

  def __str__(self):
    targets = ", ".join([str(target) for target in self.targets])
    return "%s(%s, %s)" %(self.__class__.__name__, self.player, targets)

  @property
  def target(self):
    return self.targets[0]

  @target.setter
  def set_target(self, target):
    self.targets[0] = target

  @property
  def blocked(self):
    return self.player.blocked and self.player.role.blockable

  def resolve(self, game):
    # Apply roleblocking
    if self.blocked:
      game.log.append(WasBlocked(self.player))
      return

    # Apply busdriving
    self.targets = TargetList([t.switched_with for t in self.targets])

    # Record visit
    for target, raw_target in zip(self.targets, self.raw_targets):
      game.log.append(Visited(self.player, target,
                              visible=self.player.role.visible,
                              original_target=raw_target))

    # Apply protection
    if self.protectable and self.target.protected and self.player.role.protectable:
      game.log.append(Saved(target))
      return

    # Resolve action
    self._resolve(game)

  def resolve_post(self, game):
    if self.blocked: return
    self._resolve_post(game)

  def _resolve(self, game):
    pass

  def _resolve_post(self, game):
    pass

  def concrete_action(self):
    return self

class Kill(Action):
  precedence = 1000
  protectable = True

  def _resolve(self, game):
    self.target.alive = False
    game.log.append(Died(self.target))

class Protect(Action):
  precedence = 200

  def _resolve(self, game):
    self.target.add_effect(Protected())

class Investigate(Action):
  precedence = 200

  def _resolve(self, game):
    game.log.append(TurntUp(self.target.alignment, to=self.player))

def send_targets(visits, *, to, log):
  targets = set(v.target for v in visits)
  for target in sorted(targets):
    log.append(SawVisit(target, to=to))

class Track(Action):
  precedence = 2000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_by(self.target)
    send_targets(visits, to=self.player, log=game.log)

def send_visitors(visits, *, to, log):
  visitors = set(v.player for v in visits if v.player is not to)
  for visitor in sorted(visitors):
    log.append(SawVisitor(visitor, to=to))

class Watch(Action):
  precedence = 2000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_to(self.target)
    send_visitors(visits, to=self.player, log=game.log)

class Autopsy(Action):
  precedence = 200

  def _resolve(self, game):
    visits = game.log.visits_to(self.target)
    send_visitors(visits, to=self.player, log=game.log)

class Roleblock(Action):
  precedence = 100

  def _resolve(self, game):
    self.target.add_effect(Blocked())

class Busdrive(Action):
  precedence = 0

  def __init__(self, player, target1, target2):
    super().__init__(player, [target1, target2])

  def _resolve(self, game):
    a = self.targets[0]
    b = self.targets[1]
    a.add_effect(SwitchedWith(b))
    b.add_effect(SwitchedWith(a))
