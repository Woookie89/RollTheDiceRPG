import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './assets/css/tailwind.css';
import MainPage from './components/MainPage';
import Login from './components/Login';
import Navbar from './components/Navbar';
import Logout from './components/Logout.jsx';
import { UserContext } from './context/UserContext';

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
        <UserContext.Provider value={{ user, setUser, loggedIn }}>
            <Router>
                <Navbar />
                <Routes>
                    <Route path="/" element={<MainPage />} />
                    <Route
                        path="/login"
                        element={<Login handleLogin={handleLogin} />}
                    />
                    <Route path="/logout" element={<Logout />} />
                </Routes>
            </Router>
        </UserContext.Provider>
    );
}

export default App;