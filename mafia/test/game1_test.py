from mafia import *
from .test_game import TestGame

def test_game1():
  g = TestGame()
  town    = g.add_faction(Town())
  masons  = g.add_faction(Masonry("Test Team", town))
  mafia   = g.add_faction(Mafia("VMX Mafia"))
  asmar    = g.add_player("Asmar", Godfather(mafia))
  brian    = g.add_player("Brian", Watcher(town))
  calder   = g.add_player("Calder", DoubleVoter(town))
  dave     = g.add_player("Dave", Ventriloquist(mafia))
  devin    = g.add_player("Devin", Politician(town))
  doug     = g.add_player("Doug", Villager(town))
  fejta    = g.add_player("Fejta", Tracker(town))
  gijosh   = g.add_player("GI Josh", Cop(town))
  josh     = g.add_player("Josh", Mason(masons))
  justin   = g.add_player("Justin", Watcher(town))
  kim      = g.add_player("Kim", Villager(town))
  leese    = g.add_player("Leese", ForensicInvestigator(town))
  max      = g.add_player("Max", ActionDoubler(town))
  michelle = g.add_player("Michelle", Mason(masons))
  sahil    = g.add_player("Sahil", Busdriver(town))
  sami     = g.add_player("Sami", Goon(mafia))
  spencer  = g.add_player("Spencer", Roleblocker(town))
  tarl     = g.add_player("Tarl", Hitman(mafia))
  tony     = g.add_player("Tony", Doctor(town))
  g.begin()

  assert_equal(g.log.filter(lambda e: not isinstance(e, GotRole)), Log([
    GotFaction(masons, [josh, michelle]),
    GotFaction(mafia, [asmar, dave, sami, tarl]),
  ]))

  night0 = Night(0)
  night0.add_action(Double(max, justin))
  night0.add_action(FactionAction(mafia, Kill(asmar, max)))
  night0.add_action(Investigate(gijosh, tony))
  night0.add_action(Protect(tony, asmar))
  g.resolve(night0)

  assert_equal(g.log.phase(night0), Log([
    Visited(max, justin),
    Visited(gijosh, tony),
    TurntUp(Alignment.good, to=gijosh),
    Visited(tony, asmar),
    Visited(asmar, max),
    Died(max),
  ], phase=night0))
  assert max.alive is False

  day1 = Day(1)
  day1.set_vote(asmar, doug)
  day1.set_vote(brian, asmar)
  day1.set_vote(calder, doug)
  day1.set_vote(doug, asmar)
  g.resolve(day1)

  assert_equal(g.log.phase(day1), Log([
    VotedFor(asmar, doug),
    VotedFor(brian, asmar),
    VotedFor(calder, doug, votes=2),
    VotedFor(doug, asmar),
    Lynched(doug),
  ], phase=day1))
  assert doug.alive is False

  night1 = Night(1)
  night1.add_action(FactionAction(mafia, Kill(asmar, gijosh)))
  night1.add_action(StealVote(devin, calder))
  night1.add_action(Track(fejta, asmar))
  night1.add_action(Investigate(gijosh, asmar))
  night1.add_action(Protect(tony, gijosh))
  night1.add_action(Watch(justin, gijosh))
  night1.add_action(Watch(justin, tony))
  g.resolve(night1)

  assert_equal(g.log.phase(night1), Log([
    Visited(gijosh, asmar),
    TurntUp(Alignment.good, to=gijosh),
    Visited(tony, gijosh),
    Visited(asmar, gijosh),
    Saved(gijosh),
    Visited(devin, calder),
    Visited(fejta, asmar),
    Visited(justin, gijosh),
    Visited(justin, tony),
    SawVisit(gijosh, to=fejta),
    SawVisitor(asmar, to=justin),
    SawVisitor(tony, to=justin),
  ], phase=night1))
  assert gijosh.alive is True

  day2 = Day(2)
  day2.set_vote(devin, calder)
  day2.set_vote(doug, devin)
  day2.set_vote(calder, devin)
  day2.set_vote(gijosh, devin)
  day2.set_vote(max, devin)
  g.resolve(day2)
  assert_equal(g.log.phase(day2), Log([
    VotedFor(calder, calder, votes=2, original_vote=devin),
    VotedFor(devin, calder),
    VotedFor(gijosh, devin),
    Lynched(calder),
  ], phase=day2))
  assert calder.alive is False

  night2 = Night(2)
  night2.add_action(FactionAction(mafia, Kill(asmar, kim)))
  night2.add_action(Watch(brian, kim))
  night2.add_action(Track(fejta, tony))
  night2.add_action(Investigate(gijosh, sami))
  night2.add_action(Watch(justin, kim))
  night2.add_action(Protect(tony, kim))
  night2.add_action(Roleblock(spencer, tony))
  g.resolve(night2)

  assert_equal(g.log.phase(night2), Log([
    Visited(spencer, tony),
    Visited(gijosh, sami),
    TurntUp(Alignment.evil, to=gijosh),
    WasBlocked(tony),
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
  night4.add_action(Possess(dave, asmar, sahil))
  night4.add_action(Busdrive(sahil, sahil, sami))
  night4.add_action(FactionAction(mafia, Kill(asmar, dave)))
  night4.add_action(Roleblock(spencer, brian))
  night4.add_action(Watch(brian, spencer))
  g.resolve(night4)

  assert_equal(g.log.phase(night4), Log([
    Visited(sahil, sahil),
    Visited(sahil, sami),
    Visited(dave, asmar),
    Visited(spencer, brian),
    Visited(asmar, sami, original_target=sahil),
    Died(sami),
    WasBlocked(brian),
  ], phase=night4))
  assert sami.alive is False
  assert sahil.alive is True
