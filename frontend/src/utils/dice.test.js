import { describe, expect, test } from 'vitest';
import {
    addRollToHistory,
    MAX_ROLL_HISTORY,
    rollDie,
} from './dice';

describe('rollDie', () => {
    test('returns the lowest possible result', () => {
        expect(rollDie(20, () => 0)).toBe(1);
    });

    test('returns the highest possible result', () => {
        expect(rollDie(20, () => 0.999)).toBe(20);
    });

    test('rejects an invalid number of sides', () => {
        expect(() => rollDie(1)).toThrow(RangeError);
    });
});

describe('addRollToHistory', () => {
    test('places the newest roll first and limits the history', () => {
        const history = Array.from({ length: MAX_ROLL_HISTORY }, (_, index) => ({
            id: index + 1,
        }));
        const newestRoll = { id: 5 };

        expect(addRollToHistory(history, newestRoll)).toEqual([
            newestRoll,
            ...history.slice(0, MAX_ROLL_HISTORY - 1),
        ]);
    });
});
