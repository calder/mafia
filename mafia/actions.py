from .action_base import *
from .action_helpers import *
from .effects import *
from . import events
from .log import *
from . import placeholders
from .util import *

def busdrive_shares_target(self, other):
  return isinstance(other, Busdrive) and \
         len(set(self.targets).intersection(other.targets)) > 0

def roleblock_targetted_player(self, other):
  return isinstance(other, Roleblock) and self.player == other.target

class Action(ActionBase):
  @property
  def dependencies(self):
    return [
      roleblock_targetted_player,
      busdrive_shares_target,
    ]

  def __init__(self, player, targets, *, visible=True, **kwargs):
    if not isinstance(targets, list):
      targets = TargetList([targets])

    self.player      = player
    self.raw_targets = TargetList(targets)
    self.visible     = visible

  def __str__(self):
    targets = ", ".join([str(target) for target in self.targets])
    return "%s(%s, %s)" % (self.__class__.__name__, self.player, targets)

  def matches(self, other, **kwargs):
    return matches(self, other, player=self.player, **kwargs)

  def parse(self, s, *, game, player):
    match = re.fullmatch(r"%s (\w+)" % self.name, s)
    if not match:
      raise MalformedAction(self.help())
    target = game.player_named(match.group(1))
    if not target:
      raise InvalidPlayer(match.group(1))
    action = self.with_player(player).with_target(target)
    if not self.matches(action):
      raise IllegalAction()
    return action

  def help(self):
    return ["%s PLAYER" % self.name]

  @property
  def name(self):
    words = re.findall(r"[A-Z]+[a-z]*", self.__class__.__name__)
    return " ".join(words).lower()

  @property
  def targets(self):
    return [t.switched_with for t in self.raw_targets]

  @property
  def target(self):
    return self.targets[0]

  @property
  def raw_target(self):
    return self.raw_targets[0]

  def resolve(self, game):
    # Apply roleblocking
    if self.player.blocked:
      game.log.append(events.Blocked(self.player))
      return

    # Apply ventriloquisting
    if self.player.must_target:
      self.raw_targets[0] = self.player.must_target

    # Apply delaying
    if self.player.delayed:
      game.delayed_actions.append(self)
      game.log.append(events.Delayed(self.player))
      return

    # Record visit
    if self.visible:
      for target, raw_target in zip(self.targets, self.raw_targets):
        game.log.append(events.Visited(self.player, target,
                                       visible=self.player.role.visible,
                                       original_target=raw_target))
        self.target.on_visited(game=game, player=self.target, by=self.player)

    # Resolve action
    self._resolve(game)

  def resolve_post(self, game):
    if self.player.blocked or self.player.delayed: return
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
    visitors = set(v.player for v in visits if v.player != self.player)
    game.log.append(events.VisitorsResult(sorted(visitors), target=self.raw_target, to=self.player))

class EliteGuard(Action):
  precedence = 1001

  def _resolve(self, game):
    self.target.add_effect(GuardedBy(self.player, elite=True))

class Guard(Action):
  precedence = 1001

  def _resolve(self, game):
    self.target.add_effect(GuardedBy(self.player))

class Busdrive(Action):
  precedence = 0

  def __init__(self, player, target1, target2):
    super().__init__(player, [target1, target2])

  def parse(self, s, *, game, player):
    match = re.fullmatch(r"%s (\w+) and (\w+)" % self.name, s)
    if not match:
      raise MalformedAction(self.help())
    target1 = game.player_named(match.group(1))
    target2 = game.player_named(match.group(2))
    if not target1:
      raise InvalidPlayer(target1)
    if not target2:
      raise InvalidPlayer(target2)
    action = self.with_player(player).with_targets([target1, target2])
    if not self.matches(action):
      raise IllegalAction()
    return action

  def help(self):
    return ["%s PLAYER1 PLAYER2" % self.name]

  def _resolve(self, game):
    a = self.targets[0]
    b = self.targets[1]
    a.add_effect(SwitchedWith(b))
    b.add_effect(SwitchedWith(a))
    game.log.append(events.Busdriven(a, b))

class Delay(Action):
  precedence = 3

  def _resolve(self, game):
    self.target.add_effect(Delayed())

class Double(Action):
  precedence = 1000

  def _resolve(self, game):
    self.target.add_effect(ExtraAction())
    game.log.append(events.Doubled(self.target))

class HitmanKill(Action):
  precedence = 2000

  def _resolve(self, game):
    resolve_kill(self.player, self.target, game=game, protectable=False)

class Investigate(Action):
  precedence = 1000

  def _resolve(self, game):
    game.log.append(events.InvestigationResult(self.target.apparent_alignment, target=self.raw_target, to=self.player))

class Kill(Action):
  precedence = 2000

  def _resolve(self, game):
    resolve_kill(self.player, self.target, game=game)

class Pardon(Action):
  precedence = 1000

  def _resolve(self, game):
    self.target.add_effect(Unlynchable())

class Possess(Action):
  precedence = 1

  def __init__(self, player, puppet, new_target):
    super().__init__(player, puppet)
    self.new_target = new_target

  def _resolve(self, game):
    self.target.add_effect(MustTarget(self.new_target))

class Protect(Action):
  precedence = 1000

  def _resolve(self, game):
    self.target.add_effect(Protected())

class Roleblock(Action):
  precedence = 2

  def _resolve(self, game):
    self.target.add_effect(Blocked())

class StealVote(Action):
  precedence = 2000

  def _resolve(self, game):
    self.target.add_effect(VotesWith(self.player))

class Track(Action):
  precedence = 3000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_by(self.target)
    targets = set(v.target for v in visits)
    game.log.append(events.VisiteesResult(sorted(targets), target=self.raw_target, to=self.player))

class Watch(Action):
  precedence = 3000

  def _resolve_post(self, game):
    visits = game.log.this_phase().visits_to(self.target)
    visitors = set(v.player for v in visits if v.player is not self.player)
    game.log.append(events.VisitorsResult(sorted(visitors), target=self.raw_target, to=self.player))
