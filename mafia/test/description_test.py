from mafia import *

from unittest import TestCase

class DescriptionTest(TestCase):
  def test_all_roles_have_descriptions(self):
    """All roles must have a description."""
    for role in ROLES:
      assert isinstance(role.description, str) or \
             isinstance(role.description, property), \
             "%s.description is has type %s." % (role, type(role.description))

  def test_all_factions_have_objectives(self):
    """All factions must have an objective."""
    for faction in FACTIONS:
      assert isinstance(faction.objective, str) or \
             isinstance(faction.objective, property), \
             "%s.objective is has type %s." % (faction, type(faction.objective))
