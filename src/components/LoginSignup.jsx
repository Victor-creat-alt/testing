import React, { useState } from 'react';
import { FaUser } from 'react-icons/fa';
import { MdEmail } from 'react-icons/md';
import { FaLock } from 'react-icons/fa';
import { useNavigate, useLocation } from 'react-router-dom';
import './LoginSignup.css';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const LoginSignup = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { setAuthState } = useAuth();
  const [action, setAction] = useState('login');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });

  // Ensure userType is always set and not empty
  const userType = location.state?.userType && location.state.userType.trim() !== '' ? location.state.userType : 'student';
  const baseUrl = import.meta.env.VITE_API_URL;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log('handleSubmit called');
    console.log('User type:', userType);
    console.log('Base URL:', baseUrl);
    console.log('Form data:', formData);

    if (!userType) {
      alert('User type is missing or invalid.');
      return;
    }

    if (!baseUrl || baseUrl.trim() === '') {
      console.warn('API base URL is not set. Please check your environment variables.');
      alert('Server URL is not configured. Please contact support.');
      return;
    }

    // Prepare data payload based on action
    let data;
    if (action === 'login') {
      data = {
        email: formData.email,
        password: formData.password,
        userType: userType,
      };
    } else {
      data = {
        name: formData.name,
        email: formData.email,
        password: formData.password,
        userType: userType,
      };
    }

    try {
      if (action === 'login') {
        console.log('Sending login request with data:', data);
        const response = await axios.post(`${baseUrl}/login`, data);
        const user = response.data;
        console.log('Login response:', user);
        setAuthState({ userId: user.id, userType: user.userType });
        alert('Successfully logged in.');
        if (userType === 'student') {
          navigate('/home');
        } else {
          navigate('/dashboard');
        }
      } else {
        console.log('Sending signup request with data:', data);
        const response = await axios.post(`${baseUrl}/signup`, data);
        const user = response.data;
        console.log('Signup response:', user);
        setAuthState({ userId: user.id, userType: user.userType });
        alert('Registration successful.');
        if (userType === 'student') {
          navigate('/home');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (error) {
      console.error('Error during authentication:', error);
      if (
        error.response &&
        error.response.data &&
        error.response.data.error === 'Email already exists'
      ) {
        alert('Email already exists. Please use a different email.');
      } else if (
        error.response &&
        error.response.data &&
        error.response.data.error === 'Invalid credentials'
      ) {
        alert('Invalid email or password.');
      } else if (
        error.response &&
        error.response.data &&
        error.response.data.error
      ) {
        alert(`Error: ${error.response.data.error}`);
      } else {
        alert('An error occurred. Please try again.');
      }
    }
  };

  const toggleAction = () => {
    setAction(action === 'login' ? 'register' : 'login');
  };

  // Reusable form inputs to avoid duplication
  const FormInputs = () => (
    <>
      {action === 'register' && (
        <div className="input-box">
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <FaUser className="icon" />
        </div>
      )}
      <div className="input-box">
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <MdEmail className="icon" />
      </div>
      <div className="input-box">
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <FaLock className="icon" />
      </div>
    </>
  );

  return (
    <div className="login-container">
      <div className={`wrapper ${action === 'register' ? 'active' : ''}`}>
        {/* Login Form */}
        <div className="form-box login">
          <form onSubmit={(e) => handleSubmit(e, 'login')}>
            <h1>{userType === 'student' ? 'Student Login' : 'Instructor Login'}</h1>
            <FormInputs />
            <button type="submit">Login</button>
            <div className="register-link">
              <p>
                Don't have an account?{' '}
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    toggleAction();
                  }}
                >
                  Register
                </a>
              </p>
            </div>
          </form>
        </div>

        {/* Register Form */}
        <div className="form-box register">
          <form onSubmit={(e) => handleSubmit(e, 'register')}>
            <h1>{userType === 'student' ? 'Student Register' : 'Instructor Register'}</h1>
            <FormInputs />
            <button type="submit">Register</button>
            <div className="register-link">
              <p>
                Already have an account?{' '}
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    toggleAction();
                  }}
                >
                  Login
                </a>
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
