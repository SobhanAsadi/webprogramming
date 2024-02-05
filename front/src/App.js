import React, { Component, useState } from "react";

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from "./pages/Layout.js"
import Login from "./pages/Login.js"
import Signup from "./pages/Signup.js"
import Home from "./pages/Home.js"
import './App.css'
import Play from "./components/Play.js";

function App() {
  return (
      <div className="App">
        <BrowserRouter>
          <Routes>
              <Route path='/' element={<Layout />}>
                  <Route index element={<Home />}/>
                  <Route path='signup' element={<Signup />}/>
                  <Route path='login' element={<Login />}/>
                  <Route path='play' element={<Play />}/>
              </Route>
          </Routes>
          </BrowserRouter>
      </div>
    
  );
}

export default App;