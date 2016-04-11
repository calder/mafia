from mafia.mixin import *

from unittest import TestCase
from unittest.mock import MagicMock, call

class Base(object):
  def __init__(self):
    self.mixins = []

  @mixin("mixins")
  def bar(self): return "Base"

  @mixin_fn("mixins")
  def baz(self, *args, **kwargs): return "Base", args, kwargs

class FuncMixin(object):
  def __init__(self, value):
    self.value = value
    self.defer = False

  def __repr__(self):
    return "FuncMixin(%r)" % self.value

  def bar_fn(self, next):
    print("bar called:", self)
    if self.defer: return next()
    return self.value

  def baz_fn(self, next, *args, **kwargs):
    print("baz called:", self)
    if self.defer: return next()
    return self.value, args, kwargs

class PropMixin(object):
  def __init__(self, value):
    self.value = value
    self.bar   = value
    self.baz   = value

  def __repr__(self):
    return "PropMixin(%r)" % self.value

class MixinTest(TestCase):
  def test_base(self):
    """In the absense of mixins, the object's own value should be used."""
    base = Base()

    self.assertEqual("Base", base.bar)
    on_hit = MagicMock()
    self.assertEqual(("Base", (1, 2), {"a":3, "b":4}),
                     base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    on_hit.assert_not_called()

  def test_func_mixin(self):
    """Test basic function mixin behavior."""
    base  = Base()
    mixin = FuncMixin("Mixin")
    base.mixins.append(mixin)

    self.assertEqual("Mixin", base.bar)
    on_hit = MagicMock()
    self.assertEqual(("Mixin", (1, 2), {"a":3, "b":4}),
                     base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    on_hit.assert_called_once_with(mixin)

  def test_prop_mixin(self):
    """Test basic property mixin behavior."""
    base  = Base()
    mixin = PropMixin("Mixin")
    base.mixins.append(mixin)

    self.assertEqual("Mixin", base.bar)
    on_hit = MagicMock()
    self.assertEqual("Mixin", base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    on_hit.assert_called_once_with(mixin)

  def test_two_mixins(self):
    """
    Test multiple mixin behavior.

    Test that:
      1. Later mixins take precedence over earlier ones.
      2. Later mixins can defer to earlier ones by calling next().
    """
    base   = Base()
    mixin1 = FuncMixin("Mixin 1")
    mixin2 = FuncMixin("Mixin 2")
    base.mixins.append(mixin1)
    base.mixins.append(mixin2)

    # Second mixin should take priority.
    self.assertEqual("Mixin 2", base.bar)
    on_hit = MagicMock()
    self.assertEqual(("Mixin 2", (1, 2), {"a":3, "b":4}),
                     base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    self.assertEqual([call(mixin2)], on_hit.mock_calls)

    # Second mixin should now defer to first mixin.
    mixin2.defer = True
    self.assertEqual("Mixin 1", base.bar)
    on_hit = MagicMock()
    self.assertEqual(("Mixin 1", (1, 2), {"a":3, "b":4}),
                     base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    self.assertEqual([call(mixin1), call(mixin2)], on_hit.mock_calls)

    # Both mixins should now defer to base implementation.
    mixin1.defer = True
    self.assertEqual("Base", base.bar)
    on_hit = MagicMock()
    self.assertEqual(("Base", (1, 2), {"a":3, "b":4}),
                     base.baz(1, 2, a=3, b=4, on_mixin_hit=on_hit))
    self.assertEqual([call(mixin1), call(mixin2)], on_hit.mock_calls)
