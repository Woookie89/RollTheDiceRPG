import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import MainPage from './MainPage';

afterEach(() => {
    vi.restoreAllMocks();
});

test('allows the roll history to be cleared', () => {
    vi.spyOn(Math, 'random').mockReturnValue(0);
    render(<MainPage />);

    fireEvent.click(screen.getByRole('button', { name: 'Rzuć kością' }));

    expect(screen.getByRole('listitem')).toHaveTextContent('D20');
    expect(screen.getByRole('listitem')).toHaveTextContent('1');

    fireEvent.click(
        screen.getByRole('button', { name: 'Wyczyść historię' }),
    );

    expect(screen.queryByRole('listitem')).not.toBeInTheDocument();
    expect(
        screen.getByText('Wybierz kość i wykonaj pierwszy rzut.'),
    ).toBeInTheDocument();
});
