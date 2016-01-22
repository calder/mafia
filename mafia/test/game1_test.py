from mafia import *
from .test_game import TestGame

def test_game1():
  g = TestGame()
  town  = g.add_faction(Town())
  mafia = g.add_faction(Mafia("VMX Mafia"))
  asmar   = g.add_player("Asmar", Godfather(mafia))
  brian   = g.add_player("Brian", Watcher(town))
  calder  = g.add_player("Calder", Villager(town))
  doug    = g.add_player("Doug", Villager(town))
  fejta   = g.add_player("Fejta", Tracker(town))
  josh    = g.add_player("Josh", Cop(town))
  justin  = g.add_player("Justin", Watcher(town))
  kim     = g.add_player("Kim", Villager(town))
  leese   = g.add_player("Leese", ForensicInvestigator(town))
  sami    = g.add_player("Sami", Goon(mafia))
  sahil   = g.add_player("Sahil", Busdriver(town))
  spencer = g.add_player("Spencer", Roleblocker(town))
  tony    = g.add_player("Tony", Doctor(town))

  night0 = Night(0)
  night0.add_action(FactionAction(mafia, Kill(asmar, calder)))
  night0.add_action(Investigate(josh, tony))
  night0.add_action(Protect(tony, asmar))
  g.resolve(night0)

  assert_equal(g.log.phase(night0), Log([
    Visited(josh, tony),
    TurntUp(Alignment.good, to=josh),
    Visited(tony, asmar),
    Visited(asmar, calder),
    Died(calder),
  ], phase=night0))
  assert calder.alive is False

  day1 = Day(1)
  day1.set_vote(asmar, doug)
  day1.set_vote(brian, doug)
  day1.set_vote(doug, asmar)
  g.resolve(day1)

  assert_equal(g.log.phase(day1), Log([
    Lynched(doug),
  ], phase=day1))
  assert doug.alive is False

  night1 = Night(1)
  night1.add_action(FactionAction(mafia, Kill(asmar, josh)))
  night1.add_action(Track(fejta, asmar))
  night1.add_action(Investigate(josh, asmar))
  night1.add_action(Protect(tony, josh))
  g.resolve(night1)

  assert_equal(g.log.phase(night1), Log([
    Visited(josh, asmar),
    TurntUp(Alignment.good, to=josh),
    Visited(tony, josh),
    Visited(asmar, josh),
    Saved(josh),
    Visited(fejta, asmar),
    SawVisit(josh, to=fejta),
  ], phase=night1))
  assert josh.alive is True

  night2 = Night(2)
  night2.add_action(FactionAction(mafia, Kill(asmar, kim)))
  night2.add_action(Watch(brian, kim))
  night2.add_action(Track(fejta, tony))
  night2.add_action(Investigate(josh, sami))
  night2.add_action(Watch(justin, kim))
  night2.add_action(Protect(tony, kim))
  night2.add_action(Roleblock(spencer, tony))
  g.resolve(night2)

  assert_equal(g.log.phase(night2), Log([
    Visited(spencer, tony),
    Visited(josh, sami),
    TurntUp(Alignment.evil, to=josh),
    Blocked(tony),
    Visited(asmar, kim),
    Died(kim),
    Visited(brian, kim),
    Visited(fejta, tony),
    Visited(justin, kim),
    SawVisitor(asmar, to=brian),
    SawVisitor(justin, to=brian),
    SawVisitor(asmar, to=justin),
    SawVisitor(brian, to=justin),
  ], phase=night2))
  assert kim.alive is False

  night3 = Night(3)
  night3.add_action(Autopsy(leese, kim))
  g.resolve(night3)

  assert_equal(g.log.phase(night3), Log([
    Visited(leese, kim),
    SawVisitor(asmar, to=leese),
    SawVisitor(brian, to=leese),
    SawVisitor(justin, to=leese),
  ], phase=night3))

  night4 = Night(4)
  night4.add_action(Busdrive(sahil, sahil, sami))
  night4.add_action(FactionAction(mafia, Kill(asmar, sahil)))
  night4.add_action(Roleblock(spencer, brian))
  night4.add_action(Watch(brian, spencer))
  g.resolve(night4)

  assert_equal(g.log.phase(night4), Log([
    Visited(sahil, sahil),
    Visited(sahil, sami),
    Visited(spencer, brian),
    Visited(asmar, sami, original_target=sahil),
    Died(sami),
    Blocked(brian),
  ], phase=night4))
  assert sami.alive is False
  assert sahil.alive is True
