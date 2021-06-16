import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
import App from './App';
import AuthContext, { AuthContextProvide } from './store/auth-context';

ReactDOM.render(
  <AuthContextProvide>
    <App />
  </AuthContextProvide>, 
  document.getElementById('root')
);
