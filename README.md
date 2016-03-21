# Mafia

This is a library for running games of [Mafia](http://wiki.mafiascum.net/).

## Installing

```sh
python3 setup.py install
```

## Running Tests

```sh
python3 setup.py test
```

## Usage

```python
from mafia import *

g = Game()

town  = g.add_faction(Town())
mafia = g.add_faction(Mafia("NSA"))

alice   = g.add_player("Alice", Doctor(town))
bob     = g.add_player("Bob", Cop(town))
charlie = g.add_player("Charlie", Vigilante(town))
eve     = g.add_player("Eve", Godfather(mafia))
malory  = g.add_player("Malory", Goon(mafia))

night0 = Night(0)
night0.add_action(Protect(alice, bob))
night0.add_action(FactionAction(mafia, Kill(eve, bob)))
night0.add_action(Investigate(bob, malory))
night0.add_action(Kill(charlie, eve))
g.resolve(night0)

print(g.log.phase(night0))

day1 = Day(1)
day1.set_vote(alice, malory)
day1.set_vote(bob, malory)
day1.set_vote(charlie, malory)
day1.set_vote(malory, bob)
g.resolve(day1)

print(g.log.phase(day1))
```

See [mafia/test/game1_test.py](mafia/test/game1_test.py) for examples of some crazier roles.

## Features / ToDo

- Mechanics
  - [x] Night resolution
    - [x] Valid action checking
    - [x] Natural action resolution
    - [x] Compelled actions
    - [X] Disjunctive actions
    - [ ] One-shot actions
  - [x] Day resolution
    - [x] Voting / lynching
    - [ ] Day actions
  - [ ] Immediate actions
  - [x] Winner calculation
  - [x] Faction actions
  - [x] Roles as modifiers (i.e. Ninja Hitman)
  - [x] Non-exclusive win conditions
- Roles
  - [x] Action Doubler
  - [x] Bodyguard
  - [ ] Bomb
  - [x] Busdriver
  - [x] Cop
  - [x] Delayer
  - [x] Doctor
  - [x] Double Voter
  - [x] Elite Bodyguard
  - [x] Forensic Investigator
  - [ ] Framer
  - [x] Goon
  - [x] Godfather
  - [x] Governor
  - [ ] Jack of All Trades
  - [ ] Jailkeeper
  - [x] Joker
  - [ ] Lover
  - [x] Lyncher
  - [x] Mason
  - [x] Miller
  - [x] Paranoid Gun Owner
  - [x] Politician
  - [x] Roleblocker
  - [x] Tracker
  - [x] Usurper
  - [x] Vengeful
  - [x] Ventriloquist
  - [x] Vigilante
  - [x] Watcher
- Role modifiers
  - [x] Hitman
  - [x] Ninja
  - [ ] One Shot
  - [x] Overeager
- Questions
  - [ ] How should a one-shot hitman work?
  - [ ] How should multi-action factions work?
