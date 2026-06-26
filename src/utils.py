from functools import wraps

WALL = 2.4
CARD_GAP = 1
SLEEVED_THICKNESS = 0.6

def stack_thickness(cards):
    """Calculates the minimum gap required for a card stack"""
    return (cards * SLEEVED_THICKNESS) + CARD_GAP

def prime(generator):
    @wraps(generator)
    def start(*args, **kwargs):
        gen = generator(*args, **kwargs)
        next(gen)
        return gen
    return start
