import React, { useState, useContext, useEffect } from 'react';

const AuthContext = React.createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider(props) {
  const storedUser = localStorage.getItem('user');
  const storedUserInfo = localStorage.getItem('userInfo');

  const [authUser, setAuthUser] = useState(storedUserInfo ? JSON.parse(storedUserInfo) : null);
  const [isLoggedIn, setIsLoggedIn] = useState(!!storedUser);

  const handleLogin = (user) => {
    localStorage.setItem('user', user.id);
    localStorage.setItem('userInfo', JSON.stringify(user));
    setAuthUser(user);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('userInfo');
    setAuthUser(null);
    setIsLoggedIn(false);
  };

  useEffect(() => {
    // You might want to perform additional initialization here
    // depending on your use case
  }, []); // Empty dependency array means it runs once on mount

  const value = {
    authUser,
    setAuthUser,
    isLoggedIn,
    setIsLoggedIn,
    handleLogin,
    handleLogout,
  };

  return (
    <AuthContext.Provider value={value}>
      {props.children}
    </AuthContext.Provider>
  );
}
