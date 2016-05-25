from mafia import *

from unittest import TestCase

class LogTest(TestCase):
  def setUp(self):
    self.test_log = Log([
      events.Visited("Alice", "Doctor", phase=START),
      events.Visited("Bob", "Cop", to="Bob"),
      events.Visited("Alice", "Bob"),
      events.Visited("Bob", "Alice"),
      events.Visited("Eve", "Alice"),
      events.Visited("Eve", "Bob", visible=False),
    ])

  def test_phase(self):
    assert_equal(self.test_log.phase(START), Log([
      events.Visited("Alice", "Doctor", phase=START),
    ]))

  def test_to(self):
    assert_equal(self.test_log.to("Bob"), Log([
      events.Visited("Bob", "Cop", to="Bob"),
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

  def test_log_addition(self):
    self.assertEqual(type(Log([]) + Log([])), Log)
