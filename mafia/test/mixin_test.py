from mafia.mixin import *

from unittest import TestCase

class Foo(object):
  def __init__(self, value):
    self.value  = value
    self.mixins = []

  @mixin("mixins")
  def bar(self): return self.value

class MixinTest(TestCase):
  def setUp(self):
    self.foo = Foo("base")

  def test_base(self):
    """In the absense of mixins, the object's own value should be used."""
    self.assertEqual("base", self.foo.bar)

  def test_mixin(self):
    """Mixins should be able to override values."""
    self.foo.mixins.append(Foo("override"))
    self.assertEqual("override", self.foo.bar)

  def test_two_mixins(self):
    """Later mixins should take precedence over earlier ones."""
    self.foo.mixins.append(Foo("override 1"))
    self.foo.mixins.append(Foo("override 2"))
    self.assertEqual("override 2", self.foo.bar)
