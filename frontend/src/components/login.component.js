import React, { useState } from "react";
import { authenticateUser } from "../services/auth.service";
import { Navigate } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleRememberMeChange = (e) => {
    setRememberMe(e.target.checked);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const result = await authenticateUser(username, password);
      console.log(result.message);
      if (result.message === "Authentification réussie") {
        setSuccess(true); // Set success status
        setError(""); // Reset error message
        window.location = "/dashboard";
      } else {
        setError("Login failed"); // Set error message
        setSuccess(false); // Reset success status
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Sign In</h3>
      {error && (
        <center>
          <div className="error">login non successful</div>
        </center>
      )}
      {success && (
        <center>
          <div className="success">Login successful!</div>
        </center>
      )}
      <div className="mb-3">
        <label>Username</label>
        <input
          type="text"
          className="form-control"
          placeholder="Enter username"
          value={username}
          onChange={handleUsernameChange}
        />
      </div>
      <div className="mb-3">
        <label>Password</label>
        <input
          type="password"
          className="form-control"
          placeholder="Enter password"
          value={password}
          onChange={handlePasswordChange}
        />
      </div>
      <div className="mb-3">
        <div className="custom-control custom-checkbox">
          <input
            type="checkbox"
            className="custom-control-input"
            id="customCheck1"
            checked={rememberMe}
            onChange={handleRememberMeChange}
          />
          <label className="custom-control-label" htmlFor="customCheck1">
            Remember me
          </label>
        </div>
      </div>
      <div className="d-grid">
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </div>
      <p className="forgot-password text-right">
        Forgot <a href="#">password?</a>
      </p>
    </form>
  );
}
