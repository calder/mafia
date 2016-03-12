from mafia.util import *

from unittest import TestCase

class UtilTest(TestCase):
  def test_assert_equal(self):
    assert_equal(123, 123)
    with self.assertRaises(AssertionError):
      assert_equal(123, 321)

  def test_identitydefaultdict(self):
    d = identitydefaultdict()
    assert_equal(d[123], 123)
    d[123] = 456
    assert_equal(d[123], 456)

  def test_str_list(self):
    assert_equal(str_list([], "zilch"), "zilch")
    assert_equal(str_list([1], "zilch"), "1")
    assert_equal(str_list([1,2], "zilch"), "1 and 2")
    assert_equal(str_list([1,2,3], "zilch"), "1, 2 and 3")
    assert_equal(str_list([1,2,3,4], "zilch"), "1, 2, 3 and 4")

  def test_has_method(self):
    assert has_method([1,2,3], "append")
    assert not has_method([1,2,3], "foozle")

  def test_flatten(self):
    assert_equal(flatten([]), [])
    assert_equal(flatten([[]]), [])
    assert_equal(flatten([[], []]), [])
    assert_equal(flatten([[], [1]]), [1])
    assert_equal(flatten([[1], [2, 3]]), [1,2,3])
    assert_equal(flatten([[1, 2], [3]]), [1,2,3])
