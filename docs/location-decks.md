# Location Deck Reference

Lookup data for sizing the location card boxes. Card counts derived from the
official Errata/FAQ Location Index (`~/Documents/DOS Rules/DOS_BoardGame_Errata_Faq.pdf`,
"Location Index", last page): each location's deck runs from its title card's ID
to the next title card's ID. Deck count includes the title card.

## Totals

| Source | Location cards | Decks | Notes |
|---|---|---|---|
| Base game | 486 | 46 + tutorial | 472 numbered (#1-472) + 14 tutorial |
| Haunted Keep | 45 | 5 | ~9 cards/deck avg |
| Nemesis | 32 | 5 | ~6.4 cards/deck avg |
| Dungeon/Nightmare | 0 | — | uses Formation Cards, no location decks |
| **Total** | **563** | **~57** | |

## Base game decks (official index, verified)

Deck size = next start # − start #. Battlefield assumes final card is #472
(reconciles: 472 + 14 tutorial = 486 stated total).

| Atlas pg | Location | Start # | Cards |
|---|---|---|---|
| 3 | Shipwreck | 1 | 12 |
| 4 | Upper Beach | 13 | 12 |
| 5 | Fort Joy Entrance | 25 | 16 |
| 6 | Smugglers' Ship | 41 | 7 |
| 7 | Arena | 48 | 9 |
| 8 | Magister's Quarters | 57 | 14 |
| 9 | Cliff Passages | 71 | 11 |
| 10 | Dungeon | 82 | 13 |
| 11 | Front Courtyard | 95 | 8 |
| 12 | Drawbridge | 103 | 8 |
| 13 | Secret Lab | 111 | 13 |
| 14 | Lava Caves | 124 | 22 |
| 15 | Underground Ruins | 146 | 17 |
| 16 | Hidden Docks | 163 | 11 |
| 17 | City Foundations | 174 | 11 |
| 18 | Swamp | 185 | 9 |
| 19 | Bountiful Forest | 194 | 12 |
| 20 | Wilderness Trail | 206 | 16 |
| 21 | Swamp Trail | 222 | 26 |
| 22 | Coastline | 248 | 12 |
| 23 | Hermit | 260 | 6 |
| 24 | Abandoned Hut | 266 | 10 |
| 25 | Destroyed Base | 276 | 10 |
| 26 | Aquatic Cave | 286 | 13 |
| 27 | Mount Cor | 299 | 14 |
| 28 | Secret Entrance | 313 | 12 |
| 29 | Forest Heart | 325 | 4 |
| 30 | Hall of Echoes | 329 | 6 |
| 31 | Magisters' Camp | 335 | 8 |
| 32 | Dragon Field | 343 | 6 |
| 33 | Braccus Rex Tomb | 349 | 7 |
| 34 | Path to Shore | 356 | 7 |
| 35 | Seekers' Base | 363 | 9 |
| 36 | Destroyed Seekers' Base | 372 | 10 |
| 37 | Gareth Rescue | 382 | 9 |
| 38 | Magisters' Watchtower | 391 | 4 |
| 39 | Source Well | 395 | 8 |
| 40 | Ramparts | 403 | 9 |
| 41 | Smugglers' Landing | 412 | 5 |
| 42 | Deep Sea | 417 | 6 |
| 43 | Tomb Depths | 423 | 14 |
| 44 | Guardian's Crypt | 437 | 5 |
| 45 | Frozen Fortress | 442 | 4 |
| 46 | Frozen Plains | 446 | 11 |
| 47 | Hiberheim | 457 | 7 |
| 48 | Battlefield | 464 | 9* |

\* assumes last numbered card is #472; only deck count not directly derivable
from the index.

Plus: **Tutorial deck, 14 cards** (unnumbered, separate from the index).

## Deck size distribution (box-design view)

| Stat | Value |
|---|---|
| Smallest deck | 4 (Forest Heart, Magisters' Watchtower, Frozen Fortress) |
| Largest deck | 26 (Swamp Trail) |
| Mean | ~10.3 |
| Decks ≤ 8 cards | 19 |
| Decks 9-13 | 17 |
| Decks 14+ | 10 (Magister's Quarters 14, Mount Cor 14, Tomb Depths 14, Fort Joy Entrance 16, Wilderness Trail 16, Underground Ruins 17, Lava Caves 22, Swamp Trail 26) |

The 26-card deck drives max well depth if storing per-deck.

## Acts

Official (errata, pg 1): title cards are grouped **Act 1 = levels 1-2,
Act 2 = levels 3-4, Act 3 = levels 5-6**. The factory insert's three bins
are mislabeled "Level 1/2/3" — the act grouping is the corrected sort.

Which location belongs to which act is printed on the title cards
themselves (level), NOT in the rulebook or errata index. Approximate
ranges from community data (UNVERIFIED — confirm against the physical
title cards): Act 1 ≈ #1-110s, Act 2 ≈ #110s-200s, Act 3 ≈ #206-472
(the biggest bucket by far).

**No published per-location act/level table exists** (web-researched
2026-06-05: official PDFs, BGG threads, wiki, Printables, TTS mods).
Paths to a verified mapping:
- Read levels off the physical title cards (only firsthand source)
- [BGG box-organisation thread](https://boardgamegeek.com/thread/3260518)
  + BGG files section — blocked bot access, unchecked; skim in browser
- [mychaos Card Boxes](https://www.printables.com/model/754780) sorts
  location cards into 6 level-sized boxes — per-level counts are encoded
  in the STL widths, recoverable by measurement

### Derived act grouping (NOT from physical title cards)

**DERIVED** from the navigation graph
(`~/Documents/DOS Rules/location-path.md`, firsthand transcription) +
the errata card-number order above. Physical-title-card verification
still pending — this is a best-estimate sort, not the printed levels.

Method: the graph has two hard chokepoints every campaign path crosses.
**Swamp (pg18, #185)** funnels the whole Fort Joy island half. **Hall of
Echoes (pg30, #329)** funnels everything before the endgame. Acts are cut
at these chokepoints:
- **Act 1** = everything reachable from Shipwreck without crossing Swamp.
- **Act 2** = Swamp through the feeders of Hall of Echoes.
- **Act 3** = Hall of Echoes onward (endgame branches).

These cuts produce contiguous, monotonic card-# bands (Act1 #1-174,
Act2 #185-349, Act3 #329-464), so graph structure and errata order agree.
`depth` = shortest-path hops from Shipwreck (pg3, depth 0).

Confidence:
- **high** — chokepoint act and the community range band agree.
- **med** — chokepoint+card-order agree, but the community's *approximate*
  band would place it in the adjacent act (boundary zone; verify first).

| pg | Location | # | depth | Act | Conf |
|---|---|---|---|---|---|
| 3 | Shipwreck | 1 | 0 | 1 | high |
| 4 | Upper Beach | 13 | 1 | 1 | high |
| 5 | Fort Joy Entrance | 25 | 1 | 1 | high |
| 6 | Smugglers' Ship | 41 | 2 | 1 | high |
| 7 | Arena | 48 | 2 | 1 | high |
| 8 | Magisters' Quarters | 57 | 2 | 1 | high |
| 10 | Dungeon | 82 | 2 | 1 | high |
| 11 | Front Courtyard | 95 | 2 | 1 | high |
| 9 | Cliff Passages | 71 | 3 | 1 | high |
| 12 | Drawbridge | 103 | 3 | 1 | high |
| 13 | Secret Lab | 111 | 3 | 1 | high |
| 14 | Lava Caves | 124 | 3 | 1 | med |
| 16 | Hidden Dock | 163 | 3 | 1 | med |
| 15 | Underground Ruins | 146 | 4 | 1 | med |
| 17 | City Foundations | 174 | 4 | 1 | med |
| 18 | Swamp | 185 | 4 | 2 | high |
| 19 | Bountiful Forest | 194 | 5 | 2 | high |
| 21 | Swamp Trail | 222 | 5 | 2 | med |
| 22 | Coastline | 248 | 5 | 2 | med |
| 23 | Hermit | 260 | 5 | 2 | med |
| 20 | Wilderness Trail | 206 | 6 | 2 | med |
| 24 | Abandoned Hut | 266 | 6 | 2 | med |
| 25 | Destroyed Base | 276 | 6 | 2 | med |
| 26 | Aquatic Cave | 286 | 6 | 2 | med |
| 27 | Mount Cor | 299 | 6 | 2 | med |
| 28 | Secret Entrance | 313 | 7 | 2 | med |
| 29 | Forest Heart | 325 | 7 | 2 | med |
| 31 | Magisters' Camp | 335 | 7 | 2 | med |
| 32 | Dragon Field | 343 | 7 | 2 | med |
| 33 | Braccus Rex Tomb | 349 | 7 | 2 | med |
| 30 | Hall of Echoes | 329 | 8 | 3 | high |
| 34 | Path to Shore | 356 | 9 | 3 | high |
| 35 | Seekers' Base | 363 | 9 | 3 | high |
| 36 | Destroyed Seekers' Base | 372 | 9 | 3 | high |
| 39 | Source Well | 395 | 9 | 3 | high |
| 37 | Gareth Rescue | 382 | 10 | 3 | high |
| 38 | Magisters' Watchtower | 391 | 10 | 3 | high |
| 40 | Ramparts | 403 | 10 | 3 | high |
| 43 | Tomb Depths | 423 | 10 | 3 | high |
| 47 | Hiberheim | 457 | 10 | 3 | high |
| 41 | Smugglers' Landing | 412 | 11 | 3 | high |
| 44 | Guardian's Crypt | 437 | 11 | 3 | high |
| 46 | Frozen Plains | 446 | 11 | 3 | high |
| 48 | Battlefield | 464 | 11 | 3 | high |
| 42 | Deep Sea | 417 | 12 | 3 | high |
| 45 | Frozen Fortress | 442 | 12 | 3 | high |

Derived per-act totals (base game, sleeved decks):

| Act | Decks | Cards | Card-# band |
|---|---|---|---|
| 1 | 15 | 184 | #1-174 |
| 2 | 15 | 165 | #185-349 |
| 3 | 16 | 123 | #329-464 |

Chokepoint cut vs the community's *approximate* ranges disagree only at
the two act seams (all "med" rows). The community guess pushes the seams
~1 act later than the graph does. Card order is monotonic inside each
derived act, so the errata-order signal backs the graph cut, not the
community ranges. **Hall of Echoes (#329)** is the one card whose number
sits inside Act 2's #-span but which the graph makes the Act 3 opener —
the single structural/numeric crossover; verify it physically first.

### Graph structure relevant to box design

- **Two clean chokepoints** = natural act-bin dividers: Swamp (pg18) and
  Hall of Echoes (pg30). A three-bin act layout maps to real campaign
  flow, not just card-# thirds.
- **Tutorial is off-graph**: pages 1-2 (Torture Chamber, Lower Hold,
  14 unnumbered cards) are not reachable from Shipwreck — keep them in a
  separate small well, pulled before play and set aside.
- **Haunted Keep (expansion)** is reachable only via Act 1/2 exits
  (Drawbridge pg12, Secret Lab pg13, City Foundations pg17) and dumps
  back into Swamp (pg18). It is an optional Act 1→2 detour, not on the
  main spine — its 5 decks can bin with Act 2 or stay in the expansion box.
- **Nemesis (expansion endgame)** hangs off Epilogue (depth 13+), past
  Battlefield/Deep Sea/Frozen Fortress. Pure Act 3 / post-campaign — bin
  with the expansion box or the tail of Act 3.
- **Endgame fans out** to three terminal-ish exits all hitting Epilogue:
  Battlefield (pg48), Deep Sea (pg42), Guardian's Crypt (pg44),
  Frozen Fortress (pg45). All Act 3; no further branching to plan around.

## Sources

- Official Errata/FAQ Location Index (local PDF, authoritative for start #s)
- Base rulebook component manifest (totals)
- [BGG: Location Card #s for ease of play](https://boardgamegeek.com/thread/3259346/location-card-s-for-ease-of-play) — note: its start #s diverge from the official errata in the back half; errata wins
- [BGG: Box organisation thread](https://boardgamegeek.com/thread/3260518/box-organisation)
