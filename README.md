# Mafia

## Dependencies

```sh
sudo pip3 install nose nose-parameterized termcolor
```

## Running Tests

```sh
nosetests
```

## To Do

- Mechanics
  - [x] Night resolution
    - [x] Valid action checking
    - [x] Natural action resolution
    - [x] Compelled actions
    - [ ] Disjunctive actions
    - [ ] One-shot actions
  - [x] Day resolution
    - [x] Voting / lynching
    - [ ] Day actions
  - [ ] Immediate actions
  - [ ] Reflex actions
  - [x] Winner calculation
  - [x] Faction actions
  - [x] Roles as modifiers (i.e. Ninja Hitman)
  - [x] Non-exclusive win conditions
- Roles
  - [x] Action Doubler
  - [x] Busdriver
  - [x] Cop
  - [ ] Delayer
  - [x] Doctor
  - [x] Double Voter
  - [x] Forensic Investigator
  - [x] Goon
  - [x] Godfather
  - [ ] Governor
  - [ ] Jack of All Trades
  - [x] Joker
  - [ ] Lovers
  - [x] Lyncher
  - [x] Mason
  - [x] Miller
  - [ ] Paranoid Gun Owner
  - [x] Politician
  - [x] Roleblocker
  - [x] Tracker
  - [x] Usurper
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
