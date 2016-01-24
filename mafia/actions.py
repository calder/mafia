from .action_base import *
from .effects import *
from .events import *
from .log import *
from .placeholders import *
from .util import *

import copy

class Action(ActionBase):
  protectable = False
  dependencies = [
    lambda s, o: isinstance(o, Roleblock) and s.player == o.target,
    lambda s, o: isinstance(o, Busdrive) and len(set(s.targets).intersection(o.targets)) > 0,
  ]

  def __init__(self, player, targets, **kwargs):
    if not isinstance(targets, list):
      targets = TargetList([targets])

    self.player      = player
    self.raw_targets = TargetList(targets)
    self.targets     = TargetList(targets)

    # Prevent accidental modification of a class's prototypical dependencies
    self.dependencies = copy.deepcopy(self.dependencies)

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

  def depends_on(self, other):
    return any([d(self, other) and other != self for d in self.dependencies])

class Autopsy(Action):
  precedence = 200

  def _resolve(self, game):
    visits = game.log.visits_to(self.target)
    visitors = set(v.player for v in visits if v.player is not self.player)
    for visitor in sorted(visitors):
      game.log.append(SawVisitor(visitor, to=self.player))

class Busdrive(Action):
  precedence = 0

  def __init__(self, player, target1, target2):
    super().__init__(player, [target1, target2])

  def _resolve(self, game):
    a = self.targets[0]
    b = self.targets[1]
    a.add_effect(SwitchedWith(b))
    b.add_effect(SwitchedWith(a))

class Investigate(Action):
  precedence = 200

  def _resolve(self, game):
    game.log.append(TurntUp(self.target.alignment, to=self.player))

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

class Roleblock(Action):
  precedence = 100

  def _resolve(self, game):
    self.target.add_effect(Blocked())

class StealVote(Action):
  precedence = 1100

  def _resolve(self, game):
    self.player.add_effect(ReplaceVotes(self.player.votes + self.target.votes))
    self.target.add_effect(ReplaceVotes(0))

class Track(Action):
  precedence = 2000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_by(self.target)
    targets = set(v.target for v in visits)
    for target in sorted(targets):
      game.log.append(SawVisit(target, to=self.player))

class Watch(Action):
  precedence = 2000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_to(self.target)
    visitors = set(v.player for v in visits if v.player is not self.player)
    for visitor in sorted(visitors):
      game.log.append(SawVisitor(visitor, to=self.player))
