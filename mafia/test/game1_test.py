from mafia import *
from .util import *

def test_game1():
  g = LoggingGame()

  town     = g.add_faction(Town())
  masons   = g.add_faction(Masonry("Test Team", town))
  mafia    = g.add_faction(Mafia("VMX Mafia"))

  alex     = g.add_player("Alex", Bodyguard(town))
  alphago  = g.add_player("AlphaGo", ParanoidGunOwner(town))
  andy     = g.add_player("Andy", Governor(town))
  asmar    = g.add_player("Asmar", Godfather(mafia))
  becky    = g.add_player("Becky", Joker())
  brian    = g.add_player("Brian", Bulletproof(Watcher(town)))
  calder   = g.add_player("Calder", DoubleVoter(town))
  dave     = g.add_player("Dave", Unlynchable(Ventriloquist(mafia)))
  derek    = g.add_player("Derek", Vigilante(town))
  devin    = g.add_player("Devin", Politician(town))
  doug     = g.add_player("Doug", Villager(town))
  fejta    = g.add_player("Fejta", Tracker(town))
  gijosh   = g.add_player("GI Josh", Cop(town))
  hung     = g.add_player("Hung", Lyncher(doug))
  josh     = g.add_player("Josh", Villager(masons))
  justin   = g.add_player("Justin", Watcher(town))
  kim      = g.add_player("Kim", Vengeful(Miller(town)))
  leese    = g.add_player("Leese", ForensicInvestigator(town))
  max      = g.add_player("Max", ActionDoubler(town))
  michelle = g.add_player("Michelle", Villager(masons))
  paul     = g.add_player("Paul", Ninja(Hitman(mafia)))
  sahil    = g.add_player("Sahil", Busdriver(town))
  sami     = g.add_player("Sami", Goon(mafia))
  scott    = g.add_player("Scott", EliteBodyguard(masons))
  spencer  = g.add_player("Spencer", Roleblocker(town))
  tarl     = g.add_player("Tarl", Hitman(mafia))
  tony     = g.add_player("Tony", Doctor(town))
  tyler    = g.add_player("Tyler", Delayer(town))
  wac      = g.add_player("Wac", Goon(mafia))

  assert_equal(mafia.members(game=g), [asmar, dave, paul, sami, tarl, wac])

  g.begin()

  assert_equal(g.log.filter(lambda e: not isinstance(e, events.RoleAnnouncement)), Log([
    events.FactionAnnouncement(masons, [josh, michelle, scott]),
    events.FactionAnnouncement(mafia, [asmar, dave, paul, sami, tarl, wac]),
    events.FactionLeaderAnnouncement(mafia, asmar),
  ], phase=START))

  night0 = Night(0)
  night0.add_action(Guard(alex, max))
  night0.add_action(Kill(derek, brian))
  night0.add_action(EliteGuard(scott, alex))
  night0.add_action(Double(max, justin))
  night0.add_action(FactionAction(mafia, Kill(wac, max)))
  night0.add_action(Investigate(gijosh, josh))
  night0.add_action(Protect(tony, asmar))
  g.resolve(night0)

  assert_equal(g.log.phase(night0), Log([
    events.Visited(max, justin),
    events.ExtraAction(justin),
    events.Visited(gijosh, josh),
    events.Visited(tony, asmar),
    events.Visited(alex, max),
    events.Visited(scott, alex),
    events.Visited(derek, brian),
    events.Protected(brian),
    events.Visited(wac, max),
    events.Protected(max),
    events.Protected(alex),
    events.Died(scott),
    events.Died(wac),
    events.InvestigationResult(Alignment.good, target=josh, to=gijosh),
  ], phase=night0))
  assert max.alive
  assert alex.alive
  assert not scott.alive
  assert not wac.alive
  assert_equal(g.winners(), NO_WINNER_YET)

  day1 = Day(1)
  day1.set_vote(asmar, doug)
  day1.set_vote(brian, asmar)
  day1.set_vote(calder, doug)
  day1.set_vote(doug, asmar)
  g.resolve(day1)

  assert_equal(g.log.phase(day1), Log([
    events.VotedFor(asmar, doug),
    events.VotedFor(brian, asmar),
    events.VotedFor(calder, doug, votes=2),
    events.VotedFor(doug, asmar),
    events.Lynched(doug),
  ], phase=day1))
  assert not doug.alive
  assert_equal(g.winners(), [hung])
  assert not g.is_game_over()

  night1 = Night(1)
  night1.add_action(FactionAction(mafia, Kill(asmar, gijosh)))
  night1.add_action(StealVote(devin, calder))
  night1.add_action(Track(fejta, asmar))
  night1.add_action(Investigate(gijosh, asmar))
  night1.add_action(Protect(tony, gijosh))
  night1.add_action(Watch(justin, gijosh))
  night1.add_action(Watch(justin, asmar))
  night1.add_action(Watch(brian, tony))
  night1.add_action(Delay(tyler, brian))
  g.resolve(night1)

  assert_equal(g.log.phase(night1), Log([
    events.Visited(tyler, brian),
    events.Visited(fejta, asmar),
    events.Visited(gijosh, asmar),
    events.Visited(tony, gijosh),
    events.Visited(justin, gijosh),
    events.Visited(justin, asmar),
    events.Delayed(brian),
    events.Visited(asmar, gijosh),
    events.Protected(gijosh),
    events.Visited(devin, calder),
    events.VisiteesResult([gijosh], target=asmar, to=fejta),
    events.InvestigationResult(Alignment.good, target=asmar, to=gijosh),
    events.VisitorsResult([asmar, tony], target=gijosh, to=justin),
    events.VisitorsResult([fejta, gijosh], target=asmar, to=justin),
    events.NoDeaths(),
  ], phase=night1))
  assert gijosh.alive

  day2 = Day(2)
  day2.set_vote(devin, calder)
  day2.set_vote(doug, devin)
  day2.set_vote(calder, devin)
  day2.set_vote(gijosh, devin)
  g.resolve(day2)
  assert_equal(g.log.phase(day2), Log([
    events.VotedFor(calder, calder, votes=2, original_vote=devin),
    events.VotedFor(devin, calder),
    events.VotedFor(gijosh, devin),
    events.Lynched(calder),
  ], phase=day2))
  assert not calder.alive

  night2 = Night(2)
  night2.add_action(Delay(tyler, alphago))
  night2.add_action(FactionAction(mafia, Kill(asmar, kim)))
  night2.add_action(Watch(brian, kim))
  night2.add_action(Track(fejta, tony))
  night2.add_action(Investigate(gijosh, sami))
  night2.add_action(Watch(justin, kim))
  night2.add_action(Protect(tony, kim))
  night2.add_action(Roleblock(spencer, tony))
  g.resolve(night2)

  assert_equal(g.log.phase(night2), Log([
    events.Visited(spencer, tony),
    events.Visited(tyler, alphago),
    events.Died(tyler),
    events.Visited(brian, tony),
    events.Visited(brian, kim),
    events.Visited(fejta, tony),
    events.Visited(gijosh, sami),
    events.Visited(justin, kim),
    events.Blocked(tony),
    events.Visited(asmar, kim),
    events.Died(kim),
    events.Died(asmar),
    events.FactionLeaderAnnouncement(mafia, dave),
    events.VisitorsResult([fejta, spencer], target=tony, to=brian),
    events.VisitorsResult([asmar, justin], target=kim, to=brian),
    events.VisiteesResult([], target=tony, to=fejta),
    events.InvestigationResult(Alignment.evil, target=sami, to=gijosh),
    events.VisitorsResult([asmar, brian], target=kim, to=justin),
  ], phase=night2))
  assert not kim.alive
  assert not asmar.alive

  day3 = Day(3)
  day3.set_vote(dave, sami)
  day3.set_vote(justin, dave)
  day3.set_vote(sami, dave)
  g.resolve(day3)

  assert_equal(g.log.phase(day3), Log([
      events.VotedFor(dave, sami),
      events.VotedFor(justin, dave),
      events.VotedFor(sami, dave),
      events.NoLynch(),
  ], phase=day3))
  assert dave.alive

  night3 = Night(3)
  night3.add_action(Autopsy(leese, kim))
  g.resolve(night3)

  assert_equal(g.log.phase(night3), Log([
    events.Visited(leese, kim),
    events.VisitorsResult([asmar, brian, justin], target=kim, to=leese),
    events.NoDeaths(),
  ], phase=night3))

  day4 = Day(4)
  day4.set_vote(becky, becky)
  day4.set_vote(andy, becky)
  g.resolve(day4)

  assert_equal(g.log.phase(day4), Log([
      events.VotedFor(andy, becky),
      events.VotedFor(becky, becky),
      events.NoLynch(),
  ], phase=day4))

  night4 = Night(4)
  night4.add_action(Possess(dave, paul, dave))
  night4.add_action(Busdrive(sahil, dave, sami))
  night4.add_action(FactionAction(mafia, HitmanKill(paul, dave)))
  night4.add_action(Roleblock(spencer, brian))
  night4.add_action(Protect(tony, dave))
  night4.add_action(Watch(brian, spencer))
  g.resolve(night4)

  assert_equal(g.log.phase(night4), Log([
    events.Visited(sahil, dave),
    events.Visited(sahil, sami),
    events.Busdriven(dave, sami),
    events.Visited(dave, paul),
    events.Visited(spencer, brian),
    events.Visited(tony, sami, original_target=dave),
    events.Blocked(brian),
    events.Visited(paul, sami, visible=False, original_target=dave),
    events.Died(sami),
  ], phase=night4))
  assert not sami.alive
  assert dave.alive

  day5 = Day(5)
  day5.set_vote(becky, becky)
  g.resolve(day5)

  assert_equal(g.log.phase(day5), Log([
    events.VotedFor(becky, becky),
    events.Lynched(becky),
  ], phase=day5))
  assert_equal(g.winners(), [becky, hung])
  assert not g.is_game_over()

  night6 = Night(6)
  night6.add_action(Busdrive(sahil, dave, alex))
  night6.add_action(Guard(alex, dave))
  night6.add_action(FactionAction(mafia, HitmanKill(paul, dave)))
  g.resolve(night6)

  assert_equal(g.log.phase(night6), Log([
    events.Visited(sahil, dave),
    events.Visited(sahil, alex),
    events.Busdriven(dave, alex),
    events.Visited(alex, alex, original_target=dave),
    events.Visited(paul, alex, visible=False, original_target=dave),
    events.Died(alex),
  ], phase=night6))
