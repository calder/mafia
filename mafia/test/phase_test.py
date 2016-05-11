from mafia import *

from unittest import TestCase

class PhaseTest(TestCase):
  def test_next_phase(self):
    next = Night(123).next_phase()
    assert_equal(type(next), Day)
    assert_equal(next.number, 124)

    next = Day(123).next_phase()
    assert_equal(type(next), Night)
    assert_equal(next.number, 123)
