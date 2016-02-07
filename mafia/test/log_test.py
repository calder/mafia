from mafia.log import *

from unittest import TestCase

class LogTest(TestCase):
  def setUp(self):
    self.test_log = Log([
      events.Visited("Alice", "Bob"),
      events.Visited("Bob", "Alice"),
      events.Visited("Eve", "Alice"),
      events.Visited("Eve", "Bob", visible=False),
    ])

  def test_visits_to(self):
    assert_equal(self.test_log.visits_to("Bob"), Log([
      events.Visited("Alice", "Bob"),
    ]))

  def test_invisible_visits_to(self):
    assert_equal(self.test_log.visits_to("Bob", include_invisible=True), Log([
      events.Visited("Alice", "Bob"),
      events.Visited("Eve", "Bob", visible=False),
    ]))

  def test_visits_by(self):
    assert_equal(self.test_log.visits_by("Eve"), Log([
      events.Visited("Eve", "Alice"),
    ]))

  def test_invisible_visits_by(self):
    assert_equal(self.test_log.visits_by("Eve", include_invisible=True), Log([
      events.Visited("Eve", "Alice"),
      events.Visited("Eve", "Bob", visible=False),
    ]))
