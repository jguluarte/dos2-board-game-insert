from build123d import Color

from functools import wraps

WALL = 2.4
CARD_GAP = 1
SLEEVED_THICKNESS = 0.6

def stack_thickness(cards):
    """Calculates the minimum gap required for a card stack"""
    return (cards * SLEEVED_THICKNESS) + CARD_GAP

def prime(generator):
    @wraps(generator)
    def wrapped(*args, **kwargs):
        gen = generator(*args, **kwargs)
        next(gen)
        return gen
    return wrapped


def compiled(func):
    @wraps(func)
    def wrapped(self, *args, **kwargs):
        self.compile()
        return func(self, *args, **kwargs)
    return wrapped

def cshift(color, tint=0.3) -> Color:
    r, g, b, _ = tuple(color)

    adjust = lambda x: x + (1 - x) * tint

    return Color(
        adjust(r),
        adjust(g),
        adjust(b),
    )
