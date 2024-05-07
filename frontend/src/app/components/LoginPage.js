import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Button } from "@nextui-org/button";
import { Input } from "@nextui-org/react";
import { EyeIcon } from '@heroicons/react/24/outline';
import { EyeSlashIcon } from '@heroicons/react/24/outline';

// Load environment variables from .env.local into process.env
require('dotenv').config();

const LoginPage = () => {
  const router = useRouter(); // Use useRouter() inside the functional component
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage(''); // Clear previous messages
    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/login_user`, { username, password });
      const { token, expiration_time, user_id } = response.data;

      localStorage.setItem('token', token);
      localStorage.setItem('expiration_time', new Date(expiration_time));
      localStorage.setItem('user_id', user_id);

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

  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => setIsVisible(!isVisible);

  return (
    <div>
      <div className="flex place-content-center m-3">
        <h1>Login</h1>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="flex place-content-center m-3">
          <Input className="w-80" type="username" label="Username" placeholder="Enter your username" value={username} onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div className="flex place-content-center m-3">
          <Input
            className="w-80"
            label="Password"
            placeholder="Enter your password"
            endContent={
              <button className="focus:outline-none" type="button" onClick={toggleVisibility}>
                {isVisible ? (
                  <EyeSlashIcon className="text-2xl text-default-400" />
                ) : (
                  <EyeIcon className="text-2xl text-default-400" />
                )}
              </button>
            }
            type={isVisible ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="flex place-content-center m-3">
          <Button type="submit" color="primary" size="lg" className="text-white">Login</Button>
        </div>
        {message && <div className="text-danger">{message}</div>}
      </form>
    </div>
  );
};

export default LoginPage;