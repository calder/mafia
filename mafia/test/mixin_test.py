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
  def test_base(self):
    """In the absense of mixins, the object's own value should be used."""
    base = Foo("base")
    self.assertEqual("base", base.prop)
    self.assertEqual(("base", (1, 2), {"a":3, "b":4}),
                     base.func(1, 2, a=3, b=4))

  def test_mixin(self):
    """Mixins should be able to override values."""
    base = Foo("base")
    base.mixins.append(Foo("override"))
    self.assertEqual("override", base.prop)
    self.assertEqual(("override", (1, 2), {"a":3, "b":4}),
                     base.func(1, 2, a=3, b=4))

  def test_two_mixins(self):
    """Later mixins should take precedence over earlier ones."""
    base = Foo("base")
    base.mixins.append(Foo("override 1"))
    base.mixins.append(Foo("override 2"))
    self.assertEqual("override 2", base.prop)
    self.assertEqual(("override 2", (1, 2), {"a":3, "b":4}),
                     base.func(1, 2, a=3, b=4))
