import React from 'react';
import { Link } from 'react-router-dom';

function Navbar({ loggedIn, handleLogout }) {
    return (
        <nav className="bg-gray-800 px-8 py-4 flex justify-between">
            <div>
                <Link to="/" className="text-white text-2xl font-bold">
                    Roll The Dice RPG
                </Link>
            </div>
            <div>
                {loggedIn ? (
                    <>
                        <Link
                            to="/"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Strona Główna
                        </Link>
                        <button
                            onClick={handleLogout}
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Wyloguj
                        </button>
                    </>
                ) : (
                    <>
                        <Link
                            to="/"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Strona Główna
                        </Link>
                        <Link
                            to="/login"
                            className="text-gray-300 hover:bg-gray-700 hover:text-white px-3 py-2 rounded-md text-sm font-medium"
                        >
                            Zaloguj
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
