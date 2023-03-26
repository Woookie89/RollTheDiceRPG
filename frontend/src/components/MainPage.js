import React from 'react';
import axios from 'axios';

function MainPage() {
    const handleLoginClick = () => {
        axios
            .get('http://localhost:8000/auth/token/')
            .then(res => {
                window.location.href = '/login';
            })
            .catch(err => console.log(err));
    };

    const handleRegisterClick = () => {
        axios
            .get('http://localhost:8000/auth/token/')
            .then(res => {
                window.location.href = '/register';
            })
            .catch(err => console.log(err));
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl font-bold mb-4">ROLL THE DICE RPG</h1>
            <p className="max-w-md text-center mb-8">
                Roll The Dice RPG to prosta przeglądarkowa gra RPG
                wykorzystująca mechanikę D&D
            </p>
            <div className="text-center">
                <button
                    className="px-4 py-2 rounded-md bg-blue-500 text-white mr-4"
                    onClick={handleLoginClick}
                >
                    Log in
                </button>
                <button
                    className="px-4 py-2 rounded-md bg-green-500 text-white"
                    onClick={handleRegisterClick}
                >
                    Sign up
                </button>
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
