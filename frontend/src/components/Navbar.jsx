function Navbar({ loggedIn, handleLogout }) {
    return (
        <header className="site-header">
            <nav className="site-nav" aria-label="Główna nawigacja">
                <a href="/" className="brand-link" aria-label="Roll The Dice RPG">
                    <span className="brand-mark" aria-hidden="true">
                        20
                    </span>
                    <span>Roll The Dice RPG</span>
                </a>

                <div className="nav-actions">
                    <a href="/">Strona Główna</a>
                    {loggedIn ? (
                        <button type="button" onClick={handleLogout}>
                            Wyloguj
                        </button>
                    ) : (
                        <a href="/login" className="nav-login">
                            Zaloguj
                        </a>
                    )}
                </div>
            </nav>
        </header>
    );
}

export default Navbar;
