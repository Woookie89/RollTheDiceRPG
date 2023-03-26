import React from 'react';
import { Link } from 'react-router-dom';

function MainPage() {
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-4">ROLL THE DICE RPG</h1>
            <p className="max-w-md text-center mb-8">
                Roll The Dice RPG to prosta przeglądarkowa gra RPG
                wykorzystująca mechanikę D&amp;D
            </p>
            <div className="text-center">
                <Link
                    to="/login"
                    className="px-4 py-2 rounded-md bg-blue-500 text-white mr-4"
                >
                    Log in
                </Link>
                <Link
                    to="/register"
                    className="px-4 py-2 rounded-md bg-green-500 text-white"
                >
                    Sign up
                </Link>
            </div>
            <hr className="w-1/2 border-gray-300 my-8" />
            <div className="max-w-md">
                <h2 className="text-xl font-bold">O mnie</h2>
                <p className="my-4">
                    Elo mordko. Lorem ipsum dolor sit amet, consectetur
                    adipiscing elit. Sed auctor elit ac quam vestibulum
                    bibendum. Suspendisse potenti. Maecenas rutrum dui vel justo
                    lobortis pellentesque. Duis lobortis nunc ut neque laoreet
                    malesuada.
                </p>
            </div>
        </div>
    );
}

export default MainPage;
