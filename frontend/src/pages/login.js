import {useState} from "react";
import {Link, Navigate} from "react-router-dom";
import axios from "axios";
import useAuth from "../hooks/useAuth";
import '../styles/index.css'
import '../styles/common.css';
import logo2 from '../assets/property_images/logo2.jpeg'
export default function LoginPage() {
	const host = "http://localhost:8000";
	const [username, setusername] = useState("");
	const [password, setPassword] = useState("");
	const {isLoggedin, login} = useAuth();
	const [wrongPass, setWrongPass] = useState(false);
	const [showErr, setShowError] = useState(false);
	const [errMesg, setErrorMsg] = useState("");

	async function handleSubmit(e) {
		e.preventDefault(); //prevent the web page from automatically submitting the form after we press log in
		await requestAuth()
			.then((queryResult) => {
				console.log("it is");
				console.log(queryResult);
				if (queryResult) {
					setShowError(false);
					console.log("logging in....");
					localStorage.setItem("username", username);
					login();
				} else {
					console.log("incorect pass");
					setShowError(false);
					setWrongPass(true);
					setPassword("");
					setusername("");
				}
			})
			.catch((err) => {
				setPassword("");
				setusername("");
				setShowError(true);
				setWrongPass(false);
				if (err.message === "user not found") {
					setErrorMsg(err.message);
				} else {
					setErrorMsg("an unexpected error has occured on our side, please try again later or contact the admins");
				}
			});
	}

	async function requestAuth() {
		return new Promise((resolve, reject) => {
			axios
				.get(`${host}/account/token/`, {username, password})
				.then((ret) => {
					console.log(ret.data);
					resolve(ret.data);
				})
				.catch((err) => {
					reject(new Error(err.response.data.message));
				});
		});
	}
	if (isLoggedin) {
		return <Navigate to="/" />;
	}
	return (
        <>
        <div className="container">
        <div className="row mb-3" style={{paddingTop: '0vh'}}>
            <div className="col-lg-4 col-md-3 themed-grid-col"></div>
            <div className="col-lg-4 col-md-6 themed-grid-col">
                <img src={logo2} className="d-block w-100" alt="..."></img>
            </div>
        </div>
    </div>
    <div className="container">
        <div className="row mb-3">
            <div className="col-lg-4 themed-grid-col"></div>
            <div className="col-lg-4 themed-grid-col user-form">
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="user-email" className="form-label">Username</label>
                        <input type="text" className="form-control" id="user-email" aria-describedby="emailHelp"></input>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="passwd" className="form-label">Password</label>
                        <input type="password" className="form-control" id="passwd"></input>
                    </div>
                    <div style={{display: wrongPass ? "block" : "none"}}>
                        <p className="text-red-400"> Your password is incorrect </p>
                    </div>
                    <div style={{display: showErr ? "block" : "none"}}>
                        <p className="text-red-400"> {errMesg} </p>
                    </div>
                    <button type="submit" className="btn btn-dark">Login</button>
                    <Link to="/register" className="link-secondary" style={{ paddingLeft: '1rem' }}>
                        Don't have an account? Register
                    </Link>
                </form>
            </div>
        </div>
    </div>
    </>
	);
}