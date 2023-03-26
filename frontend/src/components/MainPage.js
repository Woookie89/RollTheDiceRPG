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
        <div>
            <h1>Roll The Dice RPG</h1>
            <p>Roll The Dice RPG to prosta przeglądarkowa gra RPG wykorzystująca mechanikę D&D</p>
            <h2>O mnie</h2>
            <p>Elo mordko</p>
            <button onClick={handleLoginClick}>Log in</button>
            <button onClick={handleRegisterClick}>Sign up</button>
        </div>
    );
}

export default MainPage;
