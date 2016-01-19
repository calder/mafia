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

- Roles
  - [x] Busdriver
  - [x] Cop
  - [ ] Delayer
  - [x] Doctor
  - [x] Forensic Investigator
  - [x] Goon
  - [x] Godfather
  - [x] Hitman
  - [ ] Joker
  - [ ] Lyncher
  - [ ] Masons
  - [x] Ninja
  - [x] Roleblocker
  - [x] Tracker
  - [ ] Ventriloquist
  - [x] Watcher
- Mechanics
  - [x] Night resolution
    - [x] Valid action checking
    - [ ] Natural action resolution
    - [ ] Compelled actions
    - [ ] Disjunctive actions
    - [ ] One-shot actions
  - [ ] Day resolution
  - [x] Winner calculation
  - [x] Group actions
  - [ ] Roles as modifiers (i.e. Ninja Hitman)
