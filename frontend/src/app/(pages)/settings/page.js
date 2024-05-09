'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Input } from "@nextui-org/input";
import { Button } from "@nextui-org/button";
import axios from 'axios';

// Load environment variables from .env.local into process.env
require('dotenv').config();

export default function Settings() {
  const router = useRouter();
  const [userData, setUserData] = useState(null);
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');
    const userID = localStorage.getItem('user_id');

    if (!token || !expirationTime || Date.now() > parseInt(expirationTime)) {
      redirectToLogin();
    } else {
      axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_user/${userID}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          setUserData(response.data);
          console.log(response.data);
          setFormData({
            username: response.data.username,
            email: response.data.email,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            password: ''
          });
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    }
  }, []);

  const redirectToLogin = () => {
    window.location.href = '/login';
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userID = localStorage.getItem('user_id');
  
    axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/edit_user/${userID}`, formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        setMessage(response.data.message);
        // Clear the error message on success
        setErrorMessage('');
      })
      .catch(error => {
        setErrorMessage(error.response && error.response.data.message
          ? error.response.data.message
          : 'Sign-up failed. Please check your input and try again.');
      });
  };

  const handleChange = (name, value) => {
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: value
    }));
  };

  const formatLabel = (key) => {
    return key.replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  };

  return (
    <div className="flex justify-left">
      <div className="container mx-auto px-4">
        {/* Main Header */}
        {/* Main Header */}
        <h1 className='my-4'>Settings</h1>
        {/* Account Update Form */}
        <form onSubmit={handleSubmit}>
          <h2 className='mb-2'>Account</h2>
          <div className="grid grid-cols-1 gap-y-2">
            {userData && (
              <div>
                {Object.keys(formData).map((key, index) => (
                  <div className="group relative mb-2" key={index}>
                    <Input
                      size="md"
                      type={key === 'password' ? 'password' : (key === 'email' ? 'email' : 'text')}
                      label={formatLabel(key)}
                      placeholder={`Change ${formatLabel(key)}`}
                      value={formData[key]}
                      onChange={(e) => handleChange(key, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            )}
            <Button className="button-text" type="submit" color="primary" auto>
              Update
            </Button>
            {errorMessage && (
              <p className="text-center text-sm text-red-600 mt-1">{errorMessage}</p>
            )}
            {message && (
              <p className="text-center text-sm text-green-600 mt-1">{message}</p>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
