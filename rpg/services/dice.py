import random
import re


DICE_RE = re.compile(r'^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$')


class DiceExpressionError(ValueError):
    pass


def roll_expression(expression):
    normalized = expression.lower().replace(' ', '')
    match = DICE_RE.match(normalized)
    if not match:
        raise DiceExpressionError('Użyj zapisu typu 1d20, d100 albo 2d6+3.')

    count = int(match.group('count') or 1)
    sides = int(match.group('sides'))
    modifier = int(match.group('modifier') or 0)

    if count < 1 or count > 100:
        raise DiceExpressionError('Możesz rzucić od 1 do 100 kości naraz.')
    if sides < 2 or sides > 1000:
        raise DiceExpressionError('Kość musi mieć od 2 do 1000 ścian.')

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    return {
        'expression': normalized,
        'rolls': rolls,
        'modifier': modifier,
        'total': total,
    }
