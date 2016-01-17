from mafia import *

g = Game()
town  = g.add_faction(Town())
mafia = g.add_faction(Mafia("NSA"))
alice  = g.add_player(Player("Alice", role=Villager(faction=town)))
bob    = g.add_player(Player("Bob", role=Villager(faction=town)))
eve    = g.add_player(Player("Eve", role=Godfather(faction=mafia)))
malory = g.add_player(Player("Malory", role=Goon(faction=mafia)))

night0 = Night(0)
night0.add_action(FactionAction(mafia, Kill(malory, alice)))
g.resolve(night0)

print(g.log)
