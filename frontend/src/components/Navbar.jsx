function Navbar({ loggedIn, handleLogout }) {
    return (
        <nav className="bg-gray-800 px-8 py-4 flex justify-between">
            <div>
                <a href="/" className="text-white text-2xl font-bold">
                    Roll The Dice RPG
                </a>
            </div>
            <div>
                {loggedIn ? (
                    <>
                        <a
                            href="/"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Strona Główna
                        </a>
                        <button
                            onClick={handleLogout}
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Wyloguj
                        </button>
                    </>
                ) : (
                    <>
                        <a
                            href="/"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Strona Główna
                        </a>
                        <a
                            href="/login"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Zaloguj
                        </a>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
