import React from 'react'
import './Page.css'
import {useState} from 'react'
import hideImage from './hide.png'
import visibleImage from './visible.png'
import {useNavigate } from 'react-router-dom'


function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate=useNavigate();

    const [visibility, setVisibility] = useState("password")
    const [eye, setEye] = useState(hideImage)

    const [tabColor, setTabColor] = useState({
        userTab: "white",
        staffTab: "#f5f7fb"
    });

    const [type, setType] = useState("user")
    const [error, setError] = useState("")

    const handleLogin= () => {
        setError("")
        const myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json")


        const data = JSON.stringify({
            "username": username,
            "password": password
        })

        fetch(`http://127.0.0.1:8000/user-management/${type}/login/`,
                    {
                        method: 'POST',
                        headers: myHeaders,
                        body: data,
                        redirect: 'follow'
                    }
        ).then(response => response.json())
        .then(data => {
            if (data.status != 200) {
                setError(data.message)
            }
            else {
                navigate('/play')
            }
            console.log(data);
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
        <div className='page'>
            <div className="tabs">
                <a className="tab" onClick={() => changeTab("user")} style={{backgroundColor: tabColor.userTab , borderColor: tabColor.userTab}}>
                    <h>User</h>
                </a>
                <a className="tab" onClick={() => changeTab("staff")} style={{backgroundColor: tabColor.staffTab, borderColor: tabColor.staffTab}}>
                    <h>Staff</h>
                </a>
            </div>
            <div className="box">
                <h1> Login {type}</h1>
                <form className='form'>
                    <label>Username</label>
                    <input id='simpleInput' type="text" placeholder='Type your username' value={username} onChange={(content) => setUsername(content.target.value)}/>
                    <label>Password</label>
                    <div className="password" tabIndex={-1}>
                        <input id="passwordInput" type={visibility}  placeholder="Type your password" value={password} onChange={(content) => setPassword(content.target.value)}/>
                        <span className="eye" onClick={changeVisibility} style={{backgroundImage: `url(${eye})`}}></span>
                    </div>
                    <h className="error">{error}</h>
                    <a href='/signup'>Don't have an account?</a>
                    <button type="button" onClick={handleLogin}>Submit</button>
                </form>
            </div>
        </div>
    );
}

export default Login;