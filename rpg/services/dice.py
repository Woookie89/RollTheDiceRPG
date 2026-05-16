import random
import re


DICE_RE = re.compile(r'^(?P<count>\d*)d(?P<sides>\d+)(?P<modifier>[+-]\d+)?$')


class DiceExpressionError(ValueError):
    pass


def roll_expression(expression):
    normalized = expression.lower().replace(' ', '')
    match = DICE_RE.match(normalized)
    if not match:
        raise DiceExpressionError('Use dice notation like 1d20, d100 or 2d6+3.')

    count = int(match.group('count') or 1)
    sides = int(match.group('sides'))
    modifier = int(match.group('modifier') or 0)

    if count < 1 or count > 100:
        raise DiceExpressionError('Roll between 1 and 100 dice at once.')
    if sides < 2 or sides > 1000:
        raise DiceExpressionError('Dice must have between 2 and 1000 sides.')

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + modifier
    return {
        'expression': normalized,
        'rolls': rolls,
        'modifier': modifier,
        'total': total,
    }
