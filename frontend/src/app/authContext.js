import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check localStorage for authentication tokens on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');

    // Validate the token by ensuring expiration time is still in the future
    if (token && expirationTime && new Date(expirationTime) > new Date()) {
      setIsLoggedIn(true);
    } else {
      // Clear outdated tokens
      localStorage.removeItem('token');
      localStorage.removeItem('expiration_time');
      localStorage.removeItem('user_id');
      setIsLoggedIn(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
