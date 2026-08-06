import { useState } from 'react';
import './assets/css/tailwind.css';
import MainPage from './components/MainPage';
import Login from './components/Login';
import Navbar from './components/Navbar';
import Logout from './components/Logout';
import { UserContext } from './context/UserContext';

function CurrentPage({ handleLogin }) {
    switch (window.location.pathname) {
        case '/login':
            return <Login handleLogin={handleLogin} />;
        case '/logout':
            return <Logout />;
        default:
            return <MainPage />;
    }
}

function App() {
    const [loggedIn, setLoggedIn] = useState(false);
    const [user, setUser] = useState(null);

    const handleLogin = username => {
        setUser(username);
        setLoggedIn(true);
    };

    const handleLogout = () => {
        setUser(null);
        setLoggedIn(false);
    };

    return (
        <UserContext.Provider
            value={{ user, setUser, loggedIn, handleLogin, handleLogout }}
        >
            <Navbar loggedIn={loggedIn} handleLogout={handleLogout} />
            <CurrentPage handleLogin={handleLogin} />
        </UserContext.Provider>
    );
}

export default App;
