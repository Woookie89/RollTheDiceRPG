export const DICE_SIDES = [4, 6, 8, 10, 12, 20];
export const MAX_ROLL_HISTORY = 4;

export function rollDie(sides, random = Math.random) {
    if (!Number.isInteger(sides) || sides < 2) {
        throw new RangeError('A die must have at least two sides.');
    }

    return Math.floor(random() * sides) + 1;
}

export function addRollToHistory(history, roll, limit = MAX_ROLL_HISTORY) {
    return [roll, ...history].slice(0, limit);
}
