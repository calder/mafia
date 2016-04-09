from mafia.mixin import *

from unittest import TestCase

class Foo(object):
  def __init__(self, value):
    self.value  = value
    self.mixins = []

  @mixin("mixins")
  def prop(self): return self.value

  @mixin_func("mixins")
  def func(self, *args, **kwargs): return self.value, args, kwargs

class MixinTest(TestCase):
  def setUp(self):
    self.foo    = Foo("base")

  def test_base(self):
    """In the absense of mixins, the object's own value should be used."""
    self.assertEqual("base", self.foo.prop)
    self.assertEqual(("base", (1, 2), {"a":3, "b":4}),
                     self.foo.func(1, 2, a=3, b=4))

  def test_mixin(self):
    """Mixins should be able to override values."""
    self.foo.mixins.append(Foo("override"))
    self.assertEqual("override", self.foo.prop)
    self.assertEqual(("override", (1, 2), {"a":3, "b":4}),
                     self.foo.func(1, 2, a=3, b=4))

  def test_two_mixins(self):
    """Later mixins should take precedence over earlier ones."""
    self.foo.mixins.append(Foo("override 1"))
    self.foo.mixins.append(Foo("override 2"))
    self.assertEqual("override 2", self.foo.prop)
    self.assertEqual(("override 2", (1, 2), {"a":3, "b":4}),
                     self.foo.func(1, 2, a=3, b=4))
