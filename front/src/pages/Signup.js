import React from "react";
import { useState } from "react";
import './Page.css'
import hideImage from './hide.png'
import visibleImage from './visible.png'
import { useNavigate } from "react-router-dom";

function Signup() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [nickname, setNickname] = useState("");

    const navigate = useNavigate()

    const [visibility, setVisibility] = useState("password");
    const [eye, setEye] = useState(hideImage);

    const [tabColor, setTabColor] = useState({
        userTab: "white",
        staffTab: "#f5f7fb"
    });

    const [type, setType] = useState("user")
    const [error, setError] = useState("")

    const handleSignup = () => {
        setError("")
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json")

        const data = JSON.stringify({
            "username": username,
            "password": password,
            "nickname": nickname
        })

        fetch(`http://127.0.0.1:8000/user-management/${type}/signup/`,
                {
                    method: 'POST',
                    headers: myHeaders,
                    body: data,
                    redirect: 'follow'
                }
        ).then(response => response.json())
        .then(data => {
            if (data.status == 400) {
                setError(data.message)
            } else {
                navigate('/login')
            }
            console.log(data)
        })
    }

    const changeVisibility = () => {
        if (visibility === "password") {
            setVisibility("text")
            setEye(visibleImage)
        } else {
            setVisibility("password")
            setEye(hideImage)
        }

    }

    const changeTab = (whichTab) => {
        if (whichTab === "user") {
            setTabColor(() => {
                return {
                    userTab: "white",
                    staffTab: "#f5f7fb"
                }
            })
            setType("user")
        } else {
            setTabColor(() => {
                return {
                    userTab: "#f5f7fb",
                    staffTab: "white"
                }
            })
            setType("staff")
        }
    }

    return (
        <div className="page">
            <div className="tabs">
                <a className="tab" onClick={() => changeTab("user")} style={{backgroundColor: tabColor.userTab , borderColor: tabColor.userTab}}>
                    <h>User</h>
                </a>
                <a className="tab" onClick={() => changeTab("staff")} style={{backgroundColor: tabColor.staffTab, borderColor: tabColor.staffTab}}>
                    <h>Staff</h>
                </a>
            </div>
            <div className="box">
                <h1> Signup {type} </h1>
                <form className="form">
                    <label> Username </label>
                    <input id="simpleInput" type="text" placeholder="Type your username" value={username} onChange={(content) => setUsername(content.target.value)}/>
                    <label> Password </label>
                    <div className="password" tabIndex={-1}>
                        <input id="passwordInput" type={visibility}  placeholder="Type your password" value={password} onChange={(content) => setPassword(content.target.value)}/>
                        <span className="eye" onClick={changeVisibility} style={{backgroundImage: `url(${eye})`}}></span>
                    </div>
                    <label> Nickname </label>
                    <input id="simpleInput" type="text" placeholder="Type your nickname" value={nickname} onChange={(content) => setNickname(content.target.value)}/>
                    <h className="error">{error}</h>
                    <a href="/login"> Already a member?</a>
                    <button type="button" onClick={handleSignup}>Register</button>
                </form>
            </div>
        </div>
    );
}

export default Signup;