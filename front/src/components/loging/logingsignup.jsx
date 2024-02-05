import React, { Component, useState } from "react";
import  email_icon from '../../assets/img/email.png'
import  username_icon from '../../assets/img/username.png'
import  password_icon from '../../assets/img/password.png'

import './logingsignup.css'

function LoginSignup({setIsLoggedIn}){
    const [action,setAction]=useState("Login");
    const handleLogin = () => {
        setIsLoggedIn(true); // Set isLoggedIn to true when user logs in
      };
    return(
        <div className="container">
            <div className="header">
                <div className="text">{action}</div>
                <div className="underline"></div>
            </div>
            <div className="inputs">
                {action==="Login"?<div></div>:<div className="input">
                    <img src={username_icon} alt=""/>
                    <input type="text" placeholder="Name"/>
                </div>}
                <div className="input">
                    <img src={email_icon} alt=""/>
                    <input type="email"placeholder="Email Id"/>
                </div>
                <div className="input">
                    <img src={password_icon} alt=""/>
                    <input type="password" placeholder="Password"/>
                </div>
            </div>
            <div className="sumbit-container">
                <div className={action==="Login"?"submit gray":"submit"}onClick={()=>{setAction("Sign Up")}}>Sign Up</div>
                <div className={action==="Sign Up"?"submit gray":"submit"}onClick={handleLogin}>Login</div>
            </div>
            {action==="Sign Up"?<div></div>:
        <div className="forgot">Forgot Password?<span>click here</span></div>}
        </div>
    )
}

export default LoginSignup