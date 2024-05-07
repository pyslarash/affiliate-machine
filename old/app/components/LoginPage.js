import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Lobster } from 'next/font/google';
import Gear from '../components/Gear';

const lobster = Lobster({
  display: 'swap',
  subsets: ['latin'],
  weight: '400'
});

// Load environment variables from .env.local into process.env
require('dotenv').config();

const LoginPage = () => {
  const router = useRouter(); // Use useRouter() inside the functional component
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showGear, setShowGear] = useState(true); // State to control visibility of Gear
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(''); // Clear previous messages
    try {
      const response = await axios.post(`${process.env.BACKEND}/login_user`, { username, password });
      const { token, expiration_time, user_id } = response.data;
      
      localStorage.setItem('token', token);
      localStorage.setItem('expiration_time', new Date(expiration_time));
      localStorage.setItem('user_id', user_id);
      
      setShowGear(false);
      setMessage('Login successful! Redirecting...'); // Set a success message
      router.push('/dashboard');
    } catch (error) {
      setMessage(error.response && error.response.data.message ? error.response.data.message : 'Failed to login. Please check your credentials.');
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');

    // Check if token and expiration time exist and if the expiration time is in the future
    if (token && expirationTime && new Date(expirationTime) > new Date()) {
      setShowGear(false); // Hide Gear component if logged in and token hasn't expired
      router.push('/dashboard');
    }
  }, []);

  return (
    <div className="centered-container">
      <Gear /> {/* Assuming Gear is some form of loading or progress indicator */}
      <h1 className={`${lobster.className} login-header`}>Login</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <input placeholder="Username" type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <input placeholder="Password" type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit" className="login-button">Login</button>
        {message && <div className="message">{message}</div>}
      </form>
    </div>
  );
};

export default LoginPage;