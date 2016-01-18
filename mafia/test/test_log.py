from mafia.log import *

import unittest

class LogTest(unittest.TestCase):
  def setUp(self):
    self.test_log = Log([
      Visited("Alice", "Bob"),
      Visited("Bob", "Alice"),
      Visited("Eve", "Alice"),
      Visited("Eve", "Bob", visible=False),
    ])

  def test_visits_to(self):
    assert_equal(self.test_log.visits_to("Bob"), Log([
      Visited("Alice", "Bob"),
    ]))

  def test_invisible_visits_to(self):
    assert_equal(self.test_log.visits_to("Bob", include_invisible=True), Log([
      Visited("Alice", "Bob"),
      Visited("Eve", "Bob", visible=False),
    ]))

  def test_visits_by(self):
    assert_equal(self.test_log.visits_by("Eve"), Log([
      Visited("Eve", "Alice"),
    ]))

  def test_invisible_visits_by(self):
    assert_equal(self.test_log.visits_by("Eve", include_invisible=True), Log([
      Visited("Eve", "Alice"),
      Visited("Eve", "Bob", visible=False),
    ]))
