from mafia import *

def assert_equal(x, y):
  if x != y:
    print("--------------------1--------------------")
    print(y)
    print("--------------------2--------------------")
    print(x)
    print("-----------------------------------------")
  assert x == y

g = Game()
town = g.add_faction(Town())
mafia = g.add_faction(Mafia("VMX Mafia"))
asmar = g.add_player(Player("Asmar", role=Goon(faction=mafia)))
calder = g.add_player(Player("Calder", role=Villager(faction=town)))
josh = g.add_player(Player("Josh", role=Cop(faction=town)))
tony = g.add_player(Player("Tony", role=Doctor(faction=town)))

night0 = Night(0)
night0.add_action(asmar, Kill(calder))
night0.add_action(josh, Investigate(tony))
night0.add_action(tony, Protect(asmar))
g.resolve(night0)

assert_equal(g.log.phase(night0), Log([
  TurntUp(tony, "good", to=josh),
  Died(calder),
], phase=night0))
assert calder.alive is False

night1 = Night(1)
night1.add_action(asmar, Kill(josh))
night1.add_action(josh, Investigate(asmar))
night1.add_action(tony, Protect(josh))
g.resolve(night1)

assert_equal(g.log.phase(night1), Log([
  TurntUp(asmar, "evil", to=josh),
], phase=night1))
assert josh.alive is True
