from mafia import *

from unittest import TestCase

class RoleDescriptionTest(TestCase):
  def setUp(self):
    self.roles = [c for c in vars(mafia.roles).values()
                  if type(c) is type
                  and issubclass(c, mafia.Role)
                  and c is not Role]

  def test_all_roles_have_description(self):
    """All roles must have a description."""
    for role in self.roles:
      assert isinstance(role.description, str)
