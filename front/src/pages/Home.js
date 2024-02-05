// Home.js

import React from 'react';
import './Home.css';
import homeimage from "../assets/img/home.jfif"

function Home() {
    return (
        <div className="home">
            <h1 className='h1'>Welcome to the Ultimate Rock, Paper, Scissors Game!</h1>
            <p>Step into the arena where you can test your luck and strategy skills against the computer. The rules of the game are simple, yet the victory is satisfying:</p>
            <ul>
                <li>Rock crushes Scissors</li>
                <li>Scissors cuts Paper</li>
                <li>Paper covers Rock</li>
            </ul>
            <p>Choose your move wisely and may the odds be ever in your favor!</p>
           <p className="login-signup">Please Login/Signup then enjoy the game</p> 
           <img src={homeimage} alt="Rock, Paper, Scissors" className="home-image"/>
        </div>
    );
}

export default Home;
