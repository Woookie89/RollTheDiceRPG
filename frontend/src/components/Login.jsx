import React, { useState, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../context/UserContext';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const { setUser } = useContext(UserContext);

    const handleSubmit = event => {
        event.preventDefault();
        axios
            .post('http://localhost:8000/users/profile/', { username, password })
            .then(response => {
                setUser(response.data);
                window.location.href = '/profile';
            })
            .catch(error => {
                console.log(error.response.data);
            });
    };

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-2xl font-bold mb-6">Logowanie</h1>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label
                            htmlFor="username"
                            className="block font-medium text-gray-700"
                        >
                            Nazwa użytkownika
                        </label>
                        <input
                            type="text"
                            id="username"
                            name="username"
                            value={username}
                            onChange={event => setUsername(event.target.value)}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                            required
                        />
                    </div>

                    <div>
                        <label
                            htmlFor="password"
                            className="block font-medium text-gray-700"
                        >
                            Hasło
                        </label>
                        <input
                            type="password"
                            id="password"
                            name="password"
                            value={password}
                            onChange={event => setPassword(event.target.value)}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                            required
                        />
                    </div>

                    <div className="flex justify-end">
                        <button
                            type="submit"
                            className="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-md"
                        >
                            Zaloguj
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
