import React, { useContext, useEffect } from 'react';
import { UserContext } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const { handleLogout } = useContext(UserContext);
    const navigate = useNavigate();

    useEffect(() => {
        setTimeout(() => {
            handleLogout();
            navigate('/');
        }, 5000);
    }, [handleLogout, navigate]);

    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <p className="mb-4 text-center">
                Użytkownik został poprawnie wylogowany. Jeżeli chcesz
                powrócić na stronę główną użyj przycisku poniżej. Zostaniesz
                automatycznie przekierowany na stronę główną po 5 sekundach.
            </p>
            <button
                onClick={() => {
                    handleLogout();
                    navigate('/');
                }}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
                Powrót do strony głównej
            </button>
        </div>
    );
}

export default Logout;
