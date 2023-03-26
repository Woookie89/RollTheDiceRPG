import React from 'react';
import { useState } from 'react'; 

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    return (
        <div>
            <h1>Logowanie</h1>
            <form>
                <label>
                    Nazwa użytkownika:
                    <input
                        type="text"
                        value={username}
                        onChange={event => setUsername(event.target.value)}
                    />
                </label>
                <label>
                    Hasło:
                    <input
                        type="password"
                        value={password}
                        onChange={event => setPassword(event.target.value)}
                    />
                </label>
                <button type="submit">Zaloguj</button>
            </form>
        </div>
    );
}

export default Login;
