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
  - [x] Winner calculation
  - [x] Group actions
  - [ ] Roles as modifiers (i.e. Ninja Hitman)
- Roles
  - [x] Busdriver
  - [x] Cop
  - [ ] Delayer
  - [x] Doctor
  - [x] Double Voter
  - [x] Forensic Investigator
  - [x] Goon
  - [x] Godfather
  - [x] Hitman
  - [ ] Jack of All Trades
  - [ ] Joker
  - [ ] Lyncher
  - [ ] Mason
  - [x] Ninja
  - [x] Politician
  - [x] Roleblocker
  - [x] Tracker
  - [ ] Usurper
  - [x] Ventriloquist
  - [x] Watcher
- Role modifiers
  - [ ] One Shot
  - [ ] Overeager
- Other
  - [x] Dead people shouldn't be able to vote
  - [ ] Politicians shouldn't be able to steal dead people's votes
  - [ ] Test hitman ability
