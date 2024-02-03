import React, { Component, useState } from "react";
import Main from './components/Main.js'
import LoginSignup from './components/loging/logingsignup.jsx'

import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
    return (
      <div className="App">
        {!isLoggedIn ?
        <LoginSignup setIsLoggedIn={setIsLoggedIn}/>:
        <Main/>}
      </div>
    )
  
}

export default App;
