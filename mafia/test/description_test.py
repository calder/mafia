import mafia

from unittest import TestCase

class DescriptionTest(TestCase):
  def setUp(self):
    self.factions = self.strict_subclasses(mafia.Faction)
    self.roles    = self.strict_subclasses(mafia.Role)
    self.roles.remove(mafia.ModifierRole)

  def strict_subclasses(self, cls):
    """Return all strict subclasses of the given class in 'mafia'."""
    return [c for c in vars(mafia).values()
                     if type(c) == type
                     and issubclass(c, cls)
                     and c != cls]

  def test_all_roles_have_descriptions(self):
    """All roles must have a description."""
    for role in self.roles:
      assert isinstance(role.description, str) or \
             isinstance(role.description, property), \
             "%s.description is has type %s." % (role, type(role.description))

  def test_all_factions_have_objectives(self):
    """All factions must have an objective."""
    for faction in self.factions:
      assert isinstance(faction.objective, str) or \
             isinstance(faction.objective, property), \
             "%s.objective is has type %s." % (faction, type(faction.objective))
