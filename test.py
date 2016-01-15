from mafia import *

from termcolor import colored

def assert_equal(x, y):
  if x != y:
    print("--------------------1--------------------")
    print(y)
    print("--------------------2--------------------")
    print(x)
    print("-----------------------------------------")
  assert x == y

g = Game()
town  = g.add_faction(Town())
mafia = g.add_faction(Mafia("VMX Mafia"))
asmar   = g.add_player(Player("Asmar", role=Godfather(faction=mafia)))
brian   = g.add_player(Player("Brian", role=Watcher(faction=town)))
calder  = g.add_player(Player("Calder", role=Villager(faction=town)))
fejta   = g.add_player(Player("Fejta", role=Tracker(faction=town)))
josh    = g.add_player(Player("Josh", role=Cop(faction=town)))
justin  = g.add_player(Player("Justin", role=Watcher(faction=town)))
leese   = g.add_player(Player("Leese", role=ForensicInvestigator(faction=town)))
sami    = g.add_player(Player("Sami", role=Goon(faction=mafia)))
sahil   = g.add_player(Player("Sahil", role=Busdriver(faction=town)))
spencer = g.add_player(Player("Spencer", role=Roleblocker(faction=town)))
tony    = g.add_player(Player("Tony", role=Doctor(faction=town)))

night0 = Night(0)
night0.add_action(asmar, Kill(calder))
night0.add_action(josh, Investigate(tony))
night0.add_action(tony, Protect(asmar))
g.resolve(night0)

assert_equal(g.log.phase(night0), Log([
  Visited(josh, tony),
  TurntUp(tony, "good", to=josh),
  Visited(tony, asmar),
  Visited(asmar, calder),
  Died(calder),
], phase=night0))
assert calder.alive is False

night1 = Night(1)
night1.add_action(asmar, Kill(josh))
night1.add_action(fejta, Track(asmar))
night1.add_action(josh, Investigate(asmar))
night1.add_action(josh, Investigate(sami))
night1.add_action(tony, Protect(josh))
g.resolve(night1)

assert_equal(g.log.phase(night1), Log([
  Visited(josh, asmar),
  TurntUp(asmar, "good", to=josh),
  Visited(josh, sami),
  TurntUp(sami, "evil", to=josh),
  Visited(tony, josh),
  Visited(asmar, josh),
  Saved(josh),
  Visited(fejta, asmar),
  SawVisit(josh, to=fejta),
], phase=night1))
assert josh.alive is True

night2 = Night(2)
night2.add_action(asmar, Kill(josh))
night2.add_action(brian, Watch(josh))
night2.add_action(fejta, Track(tony))
night2.add_action(justin, Watch(josh))
night2.add_action(tony, Protect(josh))
night2.add_action(spencer, Roleblock(tony))
g.resolve(night2)

assert_equal(g.log.phase(night2), Log([
  Visited(spencer, tony),
  Blocked(tony),
  Visited(asmar, josh),
  Died(josh),
  Visited(brian, josh),
  Visited(fejta, tony),
  Visited(justin, josh),
  SawVisitor(asmar, to=brian),
  SawVisitor(justin, to=brian),
  SawVisitor(asmar, to=justin),
  SawVisitor(brian, to=justin),
], phase=night2))
assert josh.alive is False

night3 = Night(3)
night3.add_action(leese, Autopsy(josh))
g.resolve(night3)

assert_equal(g.log.phase(night3), Log([
  Visited(leese, josh),
  SawVisitor(asmar, to=leese),
  SawVisitor(brian, to=leese),
  SawVisitor(justin, to=leese),
  SawVisitor(tony, to=leese),
], phase=night3))

night4 = Night(4)
night4.add_action(sahil, Busdrive(sahil, sami))
night4.add_action(asmar, Kill(sahil))
g.resolve(night4)

assert_equal(g.log.phase(night4), Log([
  Visited(sahil, sahil),
  Visited(sahil, sami),
  Visited(asmar, sami),
  Died(sami)
], phase=night4))
assert sami.alive is False
assert sahil.alive is True

print(g.log)
print("-----------------------------------------")
print(colored("PASSED", "green"))
