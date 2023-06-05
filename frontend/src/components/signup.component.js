import React, { useState } from "react";
import { registerUser } from "../services/auth.service";

export default function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    e.preventDefault();

    registerUser(username, password)
      .then((response) => {
        console.log(response.data);
        setSuccess(true); // Registration successful
        setError(""); // Reset error message
      })
      .catch((error) => {
        console.error(error);
        setError("Registration failed"); // Set error message
        setSuccess(false); // Reset success status
      });
    if (success) {
      window.location("/dashboard");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Sign Up</h3>
      {error && <div className="error">{error}</div>}
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
      <div className="d-grid">
        <button type="submit" className="btn btn-primary">
          Sign Up
        </button>
      </div>
    </form>
  );
}
