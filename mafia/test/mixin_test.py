from mafia.mixin import *

from unittest import TestCase

class Base(object):
  def __init__(self):
    self.mixins = []

  @mixin_func("mixins")
  def bar(self, *args, **kwargs): return "Base", args, kwargs

  @mixin("mixins")
  def baz(self): return "Base"

class FuncMixin(object):
  def __init__(self, value):
    self.value = value
    self.defer = False

  def bar_fn(self, next, *args, **kwargs):
    if self.defer: return next()
    return self.value, args, kwargs

  def baz_fn(self, next):
    if self.defer: return next()
    return self.value

class AttrMixin(object):
  def __init__(self, value):
    self.bar = value
    self.baz = value

class MixinTest(TestCase):
  def test_base(self):
    """In the absense of mixins, the object's own value should be used."""
    base = Base()
    self.assertEqual(("Base", (1, 2), {"a":3, "b":4}), base.bar(1, 2, a=3, b=4))
    self.assertEqual("Base", base.baz)

  def test_func_mixin(self):
    """Test basic function mixin behavior."""
    base = Base()
    base.mixins.append(FuncMixin("Mixin"))
    self.assertEqual(("Mixin", (1, 2), {"a":3, "b":4}), base.bar(1, 2, a=3, b=4))
    self.assertEqual("Mixin", base.baz)

  def test_attr_mixin(self):
    """Test basic attribute mixin behavior."""
    base = Base()
    base.mixins.append(AttrMixin("Mixin"))
    self.assertEqual("Mixin", base.bar(1, 2, a=3, b=4))
    self.assertEqual("Mixin", base.baz)

  def test_two_mixins(self):
    """
    Test multiple mixin behavior.

    Test that:
      1. Later mixins take precedence over earlier ones.
      2. Later mixins can defer to earlier ones by calling next().
    """
    base = Base()
    mixin1 = FuncMixin("Mixin 1")
    mixin2 = FuncMixin("Mixin 2")
    base.mixins.append(mixin1)
    base.mixins.append(mixin2)

    # Second mixin should take priority.
    self.assertEqual(("Mixin 2", (1, 2), {"a":3, "b":4}), base.bar(1, 2, a=3, b=4))
    self.assertEqual("Mixin 2", base.baz)

    # Second mixin should now defer to first mixin.
    mixin2.defer = True
    self.assertEqual(("Mixin 1", (1, 2), {"a":3, "b":4}), base.bar(1, 2, a=3, b=4))
    self.assertEqual("Mixin 1", base.baz)

    # Both mixins should now defer to base implementation.
    mixin1.defer = True
    self.assertEqual(("Base", (1, 2), {"a":3, "b":4}), base.bar(1, 2, a=3, b=4))
    self.assertEqual("Base", base.baz)
