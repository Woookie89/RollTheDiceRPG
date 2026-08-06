import { render, screen } from '@testing-library/react';
import { expect, test } from 'vitest';
import App from './App';

test('renders the application landing page', () => {
    render(<App />);

    expect(
        screen.getByRole('heading', { name: /każda sesja ma swoje miejsce/i }),
    ).toBeInTheDocument();
});
