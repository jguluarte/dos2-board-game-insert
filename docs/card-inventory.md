# DOS Board Game — Card Inventory

Card-type inventory for storage planning. Base + Haunted Keep (HK) +
Nemesis (Nem) + Dungeon & Nightmare (D&N).

Source tags on every number:
- `[man]`  printed component manifest in a rulebook (most trusted)
- `[md]`   counted from NotebookLM markdown enumeration
- `[unv]`  unverified / inferred — flagged in notes
- `[bgg]`  BGG community sleeve breakdown (Aaron Bredon, thread 3208432;
           corroborated by Ryker sleeve kit). See "BGG sleeve data" below.

Size classes: **standard** 56x87 (BGG sleeve bucket 63x88), **mini** 41x63
(BGG 41x64), **location** 70x120 (already handled by location_box —
excluded from storage scope but listed).

`sleeved-now?` reflects Justin's current sleeving: location cards all
sleeved; L1 skills, L1 items, consumables, encountered minions sleeved;
everything else unsleeved so far. Sleeving changes well depth, so this
column drives box dims.

---

## Standard-size cards — the storage-relevant core

| Type | Count | Box | sleeved-now? | Notes |
| -- | -- | -- | -- | -- |
| Item Cards | 222 `[man]` | base | partial | items + consumables. items.md enumerates 207 → -15 dropped from source. L1 sleeved; see item sub-table |
| Skill Cards | 166 `[man]` | base | partial | L1 sleeved; see skill sub-table |
| Boss Tactic Cards | 139 `[man]` | base | no | by Act, see boss sub-table |
| Journal Cards | 68 `[man]` | base | no | story clue cards |
| Origin Cards | 30 `[man]` | base | no | 5 origins x 6 levels (see note) |
| Rune Cards | 18 `[man]` | base | no | double-sided |
| Source Collar Cards | 4 `[man]` | base | no | 1 per origin slot |
| Player Reference Cards | 4 `[man]` | base | no | rules quick-ref |
| Item & Summon Cards (HK) | 19 `[man]` | HK | partial | shuffle into base item/summon decks |
| Boss Tactic Cards (HK) | 8 `[man]` | HK | no | |
| Journal Cards (HK) | 3 `[man]` | HK | no | |
| Hexed Rune Cards (HK) | 2 `[man]` | HK | no | [HEX] rune type |
| Item & Summon Cards (Nem) | 16 `[man]` | Nem | partial | shuffle into base decks |
| Demonology Skill Cards (Nem) | 18 `[man]` | Nem | no | new skill school |
| Journal Cards (Nem) | 13 `[man]` | Nem | no | |
| Boss Tactic Cards (Nem) | 11 `[man]` | Nem | no | |
| Contract Cards (Nem) | 9 `[man]` | Nem | no | Demonic Contract deck |
| Formation Cards (D&N) | 44 `[man]` | D&N | no | dungeon layout |
| Dungeon Cards (D&N) | 91 `[man]` | D&N | no | enemy/reward, by level |
| Minion Modifier Cards (D&N) | 21 `[man]` | D&N | no | Nightmare modifiers |
| Reference Card (D&N) | 1 `[man]` | D&N | no | dungeon mode ref |
| Boss Modifier Card (D&N) | 1 `[man]` | D&N | no | single card |

| Minion Cards | 101 `[man]` `[bgg]` | base | partial | **standard 63x88** per BGG; encountered sleeved |
| Minion Cards (HK) | 14 `[man]` | HK | partial | standard (rolls into HK medium total) |
| Minion Cards (Nem) | 8 `[man]` | Nem | partial | standard (rolls into Nem medium total) |

**Minion size RESOLVED to standard 63x88** `[bgg]` — Aaron Bredon's BGG
breakdown lists 101 base Minion cards in the medium (63x88mm) group, not
the small (41x64) group. Earlier `[unv]` mini-size flag cleared. They are
standard stock; size them with the standard wells.

### Item sub-groupings (md cross-check of the 222 manifest)

`[md]` items.md = 180 unique entries, summed **Quantity** field = 237
(includes HK/Nem expansion items mixed in — that overshoot is roughly the
~35 HK + Nem expansion item cards, so base ~222 reconciles).

By item level `[md]` (unique-entry counts, not physical copies):

| Level | Unique | Band (errata Act labels) |
| -- | -- | -- |
| L1 | 28 | Act 1 (L1-2) |
| L2 | 15 | Act 1 |
| L3 | 13 | Act 2 (L3-4) |
| L4 | 22 | Act 2 |
| L5 | 18 | Act 3 (L5-6) |
| L6 | 23 | Act 3 |

Item types `[md]`:
- Unique items: 23 (no/odd gold value; some HK uniques unsellable)
- Consumables (4 types): Arrow 8, Grenade 9, Potion 11, Scroll 10
- Equipment by slot: One Hand 38, Two Hands 33, Trinket 25, Chest 27,
  Helmet 17 (slot strings had typos; rounded)

Consumables confirmed as **4 types** as you suspected (Arrow / Grenade /
Potion / Scroll).

### Skill sub-groupings (md cross-check of 166 manifest)

`[md]` skills.md = 92 unique entries; 8 are Demonology (Nemesis), so base
unique = 84. Manifest 166 physical cards = duplicate copies of the 84
designs (multiple copies per skill for a 4-player party). Treat 84 as
*designs*, 166 as *physical cards* — not a contradiction.

By level `[md]` (all 92 incl. Demonology): L1 25, L2 26, L3 15, L4 14, L5 12.

Schools `[md]`: 12 standard schools (Aero, Pyro, Hydro, Geo, Necro,
Polymorph, Warfare, Two-Handed, Scoundrel, Duelist, Huntsman, Summoning)
each with 4 base + 3 Advanced entries, plus Demonology (8, Nemesis) and
Source skills below.

### Source skills (separate md file)

`[md]` source-skills.md = 31 entries, all `Skill School: Source`,
levels 3 and 5 only. **No "Source Skill" line exists in any manifest** —
source skills are physically part of the 166 Skill Cards count, not a
distinct component entry. Listed here because you asked to confirm them:
they exist as a sub-group, not a separate manifest type.

### Boss tactics by Act / boss

`[md]` bosses.md = 18 bosses, summed Tactic Deck Size = 134. Manifest
totals: base 139 + HK 8 + Nem 11 = 158 boss-tactic cards. The md (134)
undercounts vs manifest — md tactic decks omit shadow/duplicate cards and
some bosses. Trust manifest for storage volume. Errata: boss tactic
cards are labeled by Act (BT-#), useful if you band the boss-tactic well.

Per-boss deck sizes `[md]` (mixed base+expansion): Evandrus 6, Ghoul 6,
Gheist 8, Deathfog Chimera 7, Slane 8, Shambling Oak 8, Khaleigha 8,
Darkhan 7, Venomwing 7, Ice Rhino 7, Dallis 6, Braccus Rex 6, Crypt
Guardian 7, Betrayer Crypt Guardian 13, Kraken 7, Nightmare Lizard 9,
Malady 7, Adramahlihk 7.

### Origins note (count disagreement)

Manifest: **30** Origin Cards `[man]` `[bgg]`. md origins.md enumerates
**10** origin characters x 6 levels = **60** card faces `[md]`. Base box
ships 5 playable origins (30 = 5 x 6). The extra 5 in the md are the
alternate / KS origins (Vali, Tanguistal, Farzanah, Cassian, + one more).
**RESOLVED to 30** `[bgg]` — Aaron Bredon's BGG breakdown lists 30 Origin
(character) cards in the base medium group. KS origins are not in the BGG
base count; budget 30 unless you specifically own and store the KS pack.

---

## Mini-size cards (41x63)

Per small_cards.md / community insert grouping. Statuses are mini and
handled by the external mychaos organizer — OUT OF SCOPE for this insert.

| Type | Count | Box | Size | sleeved-now? | Notes |
| -- | -- | -- | -- | -- | -- |
| Status Effect Cards | 137 `[man]` | base | mini | n/a | **OUT OF SCOPE** (external organizer) |
| Hexed Status Effect Cards (HK) | 2 `[man]` | HK | mini | n/a | **OUT OF SCOPE** ([HEX] statuses) |
| Demonic Status Effect Cards (Nem) | 4 `[man]` | Nem | mini | n/a | **OUT OF SCOPE** |
| Rune Cards | 18 `[man]` `[bgg]` | base | mini | no | BGG groups runes as small 41x64, NOT standard |

**Minions moved out of this table** — BGG resolves them to standard 63x88
(see standard section). They are not mini.

`[md]` minions.md = 100 entries (48 Veteran + 52 base) vs manifest 101 —
off by 1, likely one minion missing from the md enumeration. Veteran
variants are a real storage sub-grouping (base + Veteran pairs).

**Rune size correction** `[bgg]`: BGG places the 18 base Rune cards in the
small (41x64) group, not standard. The standard section above still lists
Rune Cards (18) — that row is the same physical cards; they are mini stock.
If you size a standard well from the standard table, subtract these 18.

---

## Non-card components to flag (future homes, not card-box)

| Component | Count | Box | Needs card-box? | Notes |
| -- | -- | -- | -- | -- |
| Talent Tiles | 36 `[man]` | base | **NO — tiles** | thicker punchboard; 15 L1 + 12 L2 + 9 L3 `[md]`. Need a tile tray, not a card well |
| Environment Effect Tokens | 18 `[man]` | base | no | token, supply |
| Source Tokens | 10 `[man]` | base | no | token |
| Gold Tokens | 24 `[man]` | base | no | token |
| Boss Tokens | 11 `[man]` | base | no | token |
| Key Token | 1 `[man]` | base | no | token |
| Dice | 16 `[man]` | base | no | |
| Deathfog Tokens (HK) | 7 `[man]` | HK | no | token |
| Key Tokens (Nem) | 3 `[man]` | Nem | no | token |
| Curse Tokens (Nem) | 7 `[man]` | Nem | no | token |
| Location Boards (HK) | 3 `[man]` | HK | no | large boards |
| Location Boards (Nem) | 3 `[man]` | Nem | no | large boards |
| Scorepad (D&N) | 1 `[man]` | D&N | no | paper pad |
| Booklets (Boss, Hall of Echoes, Epilogue, Atlas) | — `[man]` | base | no | books |
| Player/Minion/Boss Trays, Dials, Standees, Minis | many `[man]` | base | no | plastic |

**Talent Tiles flag:** these are tiles, not cards. They will not fit a
card well and need their own tile compartment — call out separately when
you get to the tile/token pass.

---

## Location-size cards (excluded — already handled)

| Type | Count | Box | Notes |
| -- | -- | -- | -- |
| Location Cards | 486 `[man]` | base | incl. 14 Tutorial; 472 numbered. Handled by location_box |
| Location Cards (HK) | 45 `[man]` | HK | |
| Location Cards (Nem) | 32 `[man]` | Nem | |
| Tutorial Cards | 14 `[man]` | base | **location-size**, subset of the 486 |

Tutorial cards are location-size (per your note + location-decks.md);
they live with the location stack, not a standard well.

---

## Source-disagreement log

1. **Skills 166 [man] vs 84 designs [md]** — physical-copy count vs unique
   designs. Not a contradiction; store for 166 physical.
2. **Items 222 [man] vs 180 unique / 237 qty [md]** — md mixes in HK+Nem
   items (~35), which roughly accounts for the 237 overshoot.
3. **Origins 30 [man] vs 60 faces [md]** — RESOLVED to 30 `[bgg]`. BGG
   base medium group lists 30; the 60 are md's KS alternates, not in base.
4. **Minions 101 [man] vs 100 [md]** — md missing one minion. Size RESOLVED
   to standard 63x88 `[bgg]` (not mini).
5. **Boss tactics 158 [man total] vs 134 [md]** — md omits shadow/extra
   tactic cards; trust manifest.
6. **Status 135 [bgg] vs 137 [man]** — BGG small group lists 135 base
   status cards; doc manifest says 137. 2-card gap, source unresolved
   (statuses are OUT OF SCOPE, so not chased). Runes 18 also in BGG's small
   group, which the doc had listed as standard.

---

## BGG sleeve data

Source: Aaron Bredon's community card-size breakdown on BGG (thread 3208432,
"How many and what size of sleeves"), corroborated by the Ryker DOS sleeve
kit totals (666 / 487 / 153). BGG uses 3 size buckets:

| BGG size | This doc's class | Card count (all boxes) |
| -- | -- | -- |
| 70x120 (Large) | location | 487 base+tut, +45 HK, +32 Nem |
| 63x88 (Medium) | standard | 726 base, +41 tutorial, +91 D&N, +44 HK, +66 Nem |
| 41x64 (Small) | mini | 153 base (135 status + 18 rune), +63 D&N, +4 HK, +13 Nem |

Per-box detail `[bgg]`:
- **Base medium (726):** 222 Item (items + consumables), 166 Skill,
  139 Boss Tactic, 101 Minion, 68 Journal, 30 Origin, 4 Source Collar.
  (+41 tutorial medium.)
- **Base small (153):** 135 Status, 18 Rune.
- **Base large (472 + 15 tutorial = 487):** Location + Tutorial location.
- **Nightmare Dungeon:** 91 medium, 63 small.
- **Haunted Keep:** 45 large, 44 medium, 4 small.
- **Nemesis:** 32 large, 66 medium, 13 small.

Ryker kit aggregate (sanity check): 666 medium total, 487 large, 153 small
— Ryker's 666 medium = base 726 minus the tutorial/optional cards Ryker
omits; treat as ballpark, not exact.

## AUTHORITATIVE totals — sleeve-tool census (Justin, 2026-06-06)

Sleeve-planning tool, "Default Card Set +3 Add-ons" (= base + HK + Nem +
D&N). **These supersede the thread-derived sums above where they differ.**

| Size | Qty | Class |
| -- | -- | -- |
| 63 x 88 | **857** | standard — THE box-math number |
| 41 x 64 | **244** | mini (status + rune + small expansion cards) |
| 70 x 120 | **564** | location |

Tool note: 37 of the 857 standard cards are tutorial-only (dead after the
tutorial) — candidates to store with the tutorial location box instead of
the active wells. (+1 more card note untranscribed.)

Per-expansion standard (63x88) split from the tool:

| Box | Standard cards |
| -- | -- |
| Base | **666** (857 minus the add-ons; matches Ryker's 666 medium) |
| Haunted Keep | 44 |
| Nemesis | 66 |
| Nightmare Dungeon | 81 |

- **Player Reference Cards are a different size** — excluded from the 857
  and from card-box planning entirely.
- D&N's 81 standard = **dungeon cards only** (per Justin). Formation /
  modifier cards are evidently NOT standard size (they're in the mini
  bucket) — the manifest-derived "158 standard D&N cards" above is wrong.
- Manifest said 91 Dungeon Cards vs tool's 81 — ten-card gap unresolved;
  physical count wins when the box opens.

Open discrepancies:
- **Location 564 vs errata-derived 563** (486+45+32). One card somewhere —
  possibly the Battlefield deck assumption (last card #472; could be #473)
  or a promo. Resolve when physically counting the last deck.
- Thread-derived per-box medium sums (726+41+91+44+66 = 968) overshoot the
  tool's 857 by ~111 — the per-box detail above is suspect; trust the tool
  totals, use per-box rows only as relative structure.

## Organization plan (Justin's scheme, 2026-06-06)

Expansions mix INTO categories (HK + Nem expand existing decks;
demonology joins skills); only D&N stands alone.

| Box | Contents | Rough count |
| -- | -- | -- |
| Skills | all schools + summons + demonology (minus source skills) | ~150-200 |
| Items | one box w/ level dividers OR L1 box + rest box | ~220+ |
| Consumables | one box w/ dividers OR per-category (4 types) | ~38+ |
| Character | origins + source skills + Source Vampirism + collars | ~65 |
| Minions | letter-blocks balanced for size, letters on box | 123 |
| Journal | one box, inner dividers | 84 |
| Bosses | 1-2 boxes, divider-per-boss (18 bosses) | 158 |
| Dungeon (D&N) | own box | 81 |
| Tutorial-only standards | DECISION PENDING: active wells vs tutorial box | 37 |

Counts are pre-sort estimates; categories overlap manifest lines (source
skills in skill counts). Physical sort wins.
</content>
