#!/usr/bin/env python3

import mafia

HEADER = """
Roles
-----

Roles may be stacked in most conceivable combinations. i.e. it is possible to
have a Bulletproof Unlynchable Watcher Godfather. Not that you would want to.
"""

FAKE_ACTION = mafia.SingletonValue("FAKE_ACTION", 195636807)

class FakeRole(mafia.Role):
  @property
  def action(self):
    return FAKE_ACTION

print(HEADER.strip())
print("\n")
print("| Role | Action | Description |")
print("| ---- | ------ | ----------- |")
for role in mafia.ROLES:
  exemplar = role(FakeRole(mafia.Town()))
  action = None
  if exemplar.action != FAKE_ACTION:
    action = exemplar.action
  if exemplar.faction_action:
    action = exemplar.faction_action
  if action:
    action = "*%s*" % action.__class__.__name__
  else:
    action = ""

  print("| **%s** | %s | %s |" % (role.name(), action, role.description))
