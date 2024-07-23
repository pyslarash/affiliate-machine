'use client'

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';
import { Tabs, Tab, Input, Link, Button, Card, CardBody, CardHeader } from "@nextui-org/react";
import { useAuth } from '@/app/authContext';

// Load environment variables from .env.local into process.env
require('dotenv').config();

export default function Login() {
  const router = useRouter(); // Use useRouter() inside the functional component
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [selected, setSelected] = useState("login");
  const { setIsLoggedIn } = useAuth();

  const handleSubmitLogin = async (e) => {
    e.preventDefault();
    setMessage('');
    setErrorMessage(''); // Clear previous error messages

    try {
      // Make the POST request to the backend
      const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/login_user`, { username, password });

      // Log the entire response to the console
      console.log('Login Response:', response);

      // Extract data from the response
      const { token, expiration_time, user_id } = response.data;

      // Store relevant data in localStorage
      localStorage.setItem('token', token);
      localStorage.setItem('expiration_time', new Date(expiration_time));
      localStorage.setItem('user_id', user_id);

      // Set a success message and redirect to the dashboard
      setMessage('Login successful! Redirecting...');
      router.push('/dashboard');
    } catch (error) {
      // Log the error response to the console
      if (error.response) {
        console.log('Error Response:', error.response);
      } else {
        console.log('Error:', error.message);
      }

      // Set an error message based on the response
      setErrorMessage(error.response && error.response.data.message
        ? error.response.data.message
        : 'Failed to login. Please check your credentials.');
    }
    setIsLoggedIn(true);
  };

  // Sign-up submission handler
  const handleSubmitSignUp = async (e) => {
    e.preventDefault();
    setMessage('');
    setErrorMessage(''); // Clear previous error messages

    try {
      // Make the POST request to the backend
      const response = await axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/create_user`, { username, email, password });

      // Log the entire response to the console
      console.log('Sign-Up Response:', response);

      // Set a success message indicating the account has been created
      setMessage('Sign-up successful! You can now log in.');
      setSelected("login"); // Switch to login tab
    } catch (error) {
      // Log the error response to the console
      if (error.response) {
        console.log('Error Response:', error.response);
      } else {
        console.log('Error:', error.message);
      }

      // Set an error message based on the response
      setErrorMessage(error.response && error.response.data.message
        ? error.response.data.message
        : 'Sign-up failed. Please check your input and try again.');
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');

    // Check if token and expiration time exist and if the expiration time is in the future
    if (token && expirationTime && new Date(expirationTime) > new Date()) {
      router.push('/dashboard');
    }
  }, []);

  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => setIsVisible(!isVisible);

  return (
    <div className="flex items-center justify-center h-screen">
      <div className="flex">
        <Card className="max-w-full center w-[340px] h-[450px]">
          <CardBody className="overflow-hidden">
            <Tabs
              fullWidth
              size="md"
              aria-label="Tabs form"
              selectedKey={selected}
              onSelectionChange={setSelected}
            >
              <Tab key="login" title="Login">
                <form className="flex flex-col gap-4" onSubmit={handleSubmitLogin}>
                  <Input
                    isRequired
                    label="Username"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    type="text"
                  />
                  <Input
                    isRequired
                    label="Password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                  />
                  <p className="text-center text-small">
                    Need to create an account?{" "}
                    <Link size="sm" onPress={() => setSelected("sign-up")} style={{ cursor: "pointer" }}>
                      Sign up
                    </Link>
                  </p>
                  <div className="flex gap-2 justify-end">
                    <Button type="submit" className="button-text" fullWidth color="primary">
                      Login
                    </Button>
                  </div>
                  {/* Error Message displayed in danger color */}
                  {errorMessage && (
                    <p className="text-center text-sm text-red-600 mt-1">{errorMessage}</p>
                  )}
                </form>
              </Tab>
              <Tab key="sign-up" title="Sign up">
                <form className="flex flex-col gap-4 h-[300px]" onSubmit={handleSubmitSignUp}>
                  <Input
                    isRequired
                    label="Username"
                    placeholder="Enter your username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    type="text"
                  />
                  <Input
                    isRequired
                    label="Email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    type="email"
                  />
                  <Input
                    isRequired
                    label="Password"
                    placeholder="Enter your password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    type="password"
                  />
                  <p className="text-center text-small">
                    Already have an account?{" "}
                    <Link size="sm" onPress={() => setSelected("login")} style={{ cursor: "pointer" }}>
                      Login
                    </Link>
                  </p>
                  <div className="flex gap-2 justify-end">
                    <Button type="submit" fullWidth className="button-text" color="primary">
                      Sign up
                    </Button>
                  </div>
                  {/* Error Message displayed in danger color */}
                  {errorMessage && (
                    <p className="text-center text-sm text-red-600 mt-1">{errorMessage}</p>
                  )}
                  {message && (
                    <p className="text-center text-sm text-green-600 mt-1">{message}</p>
                  )}
                </form>
              </Tab>
            </Tabs>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
