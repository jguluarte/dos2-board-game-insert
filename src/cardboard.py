from parts import Cardboard, CardboardConfig


# This tracks the space requried for each player-character.
#
# The gamebox has 4 of these. Breaking into the same partomatic element to
# give myself the flexibility to build something for us to store our current
# build or set of cards / state saving.
class PlayerConfig(CardboardConfig):
    name: str = "one"

    width: float = 360
    height: float = 125

    depth: float = 3.5

    color: str = "#a14560"

class Player(Cardboard):
    config: PlayerConfig = PlayerConfig()

    @property
    def stl_name(self):
        return f"player-{self.config.name}"

class MinionConfig(CardboardConfig):
    name: str = "a"

    width: float = 90
    height: float = 150

    depth: float = 3.5

    color: str = "#a14560"

class Minion(Cardboard):
    config: MinionConfig = MinionConfig()

    @property
    def stl_name(self):
        return f"minion-{self.config.name}"

class HallOfEchoesConfig(CardboardConfig):
    name: str = "hall-of-echoes"
    width: int = 105
    height: int = 163

    depth: int = 12

    color: str = "#58708c"

class HallOfEchoes(Cardboard):
    config: HallOfEchoesConfig = HallOfEchoesConfig()


class RoundTrackerConfig(CardboardConfig):
    name: str = "round-tracker"

    width: int = 380
    height: int = 140

    depth: int = 3
    color: str = "#854442"

class RoundTracker(Cardboard):
    config: RoundTrackerConfig = RoundTrackerConfig()


class BossTrackerConfig(CardboardConfig):
    name: str = "boss-tracker"
    width: int = 280
    height: int = 70

    depth: int = 3
    color: str = "#007f66"

class BossTracker(Cardboard):
    config: BossTrackerConfig = BossTrackerConfig()


class BossDeckConfig(CardboardConfig):
    name: str = "boss-deck"
    width: int = 95
    height: int = 150

    depth: int = 3
    color: str = "#007f66"

class BossDeck(Cardboard):
    config: BossDeckConfig = BossDeckConfig()
