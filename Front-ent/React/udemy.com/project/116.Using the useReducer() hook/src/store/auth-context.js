import React, { useState, useEffect } from 'react';

const AuthContext = React.createContext({
  isLoggedIn: false,
  onLogout: () => {},
  onLogin: (email, password) => {}
});

export const AuthContextProvide = (props) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const storedUserLoggedInInformation = localStorage.getItem('isLoggedIn');

    if (storedUserLoggedInInformation === '1') {
      setIsLoggedIn(true);
    }
  }, []);

  const logoutHander = () => {
    localStorage.removeItem('isLoggedIn')
    setIsLoggedIn(false);
  }
  const loginHandler = () => {
    localStorage.setItem('isLoggedIn','1');
    setIsLoggedIn(true);
  }

  return <AuthContext.Provider 
  value={{
    isLoggedIn: isLoggedIn,
    onLogout: logoutHander,
    onLogin: loginHandler
  }}>
    {props.children}</AuthContext.Provider>;
}

export default AuthContext;