import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { UserContext } from '../context/UserContext';

function Profile() {
    const [userData, setUserData] = useState(null);
    const { user } = useContext(UserContext);

    useEffect(() => {
        axios
            .get('http://localhost:8000/users/profile/', {
                headers: { Authorization: `Token ${user.auth_token}` },
            })
            .then(response => {
                console.log(response.data);
                setUserData(response.data);
            })
            .catch(error => console.log(error));
    }, [user]);

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h1 className="text-2xl font-bold mb-6">Profil użytkownika</h1>
                {userData ? (
                    <>
                        <div className="mb-4">
                            <strong>Imię i nazwisko:</strong> {userData.full_name}
                        </div>
                        <div className="mb-4">
                            <strong>Email:</strong> {userData.email}
                        </div>
                        <div className="mb-4">
                            <strong>Nazwa użytkownika:</strong> {userData.username}
                        </div>
                    </>
                ) : (
                    <p>Ładowanie...</p>
                )}
            </div>
        </div>
    );
}

export default Profile;
