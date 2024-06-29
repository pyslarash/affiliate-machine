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
  const [accountMessage, setAccountMessage] = useState('');
  const [accountErrorMessage, setAccountErrorMessage] = useState('');
  const [janMessage, setJanMessage] = useState('');
  const [janErrorMessage, setJanErrorMessage] = useState('');
  const [janCred, setJanCred] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: ''
  });
  const [janData, setJanData] = useState({
    jan_ip: '',
    jan_port: '',
    jan_prefix: ''
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');
    const userID = localStorage.getItem('user_id');

    if (!token || !expirationTime || Date.now() > parseInt(expirationTime)) {
      redirectToLogin();
    } else {
      // Fetch user account information
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
          // Fetch JAN credentials after fetching user data
          fetchJanCredentials(token);
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
        });
    }
  }, []);

  const redirectToLogin = () => {
    window.location.href = '/login';
  };

  const fetchJanCredentials = (token) => {
    axios.get(`${process.env.NEXT_PUBLIC_BACKEND}/get_credentials`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        if (response.status === 200) {
          const { jan_ip, jan_port, jan_prefix } = response.data;
          // JAN credentials exist, set them for editing
          setJanData({
            jan_ip,
            jan_port,
            jan_prefix
          });
          setJanCred(true);
        } else if (response.status === 404) {
          setJanCred(false);
        } else {
          console.error('Error fetching Jan.ai credentials:', response);
        }
      })
      .catch(error => {
        console.error('Error fetching Jan.ai credentials:', error);
        setJanCred(false);
      });
  };

  const handleSubmitAccount = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const userID = localStorage.getItem('user_id');

    axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/edit_user/${userID}`, formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(response => {
        setAccountMessage(response.data.message);
        // Clear the error message on success
        setAccountErrorMessage('');
      })
      .catch(error => {
        setAccountErrorMessage(error.response && error.response.data.message
          ? error.response.data.message
          : 'Update failed. Please check your input and try again.');
      });
  };

  const handleSubmitJan = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const { jan_ip, jan_port, jan_prefix } = janData;
  
    // Validation for JAN fields
    if (!jan_ip || !jan_port || !jan_prefix) {
      setJanErrorMessage('All Jan.ai fields are required.');
      return;
    }
  
    const updatedJanData = { jan_ip, jan_port, jan_prefix };
  
    // Check if JAN credentials exist
    if (!janCred) {
      // If no credentials exist, create new credentials
      axios.post(`${process.env.NEXT_PUBLIC_BACKEND}/set_credentials`, updatedJanData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          setJanMessage(response.data.message);
          setJanErrorMessage('');
          // Update janCred state or variable here if needed
        })
        .catch(error => {
          setJanErrorMessage(error.response && error.response.data.message
            ? error.response.data.message
            : 'Update failed. Please check your input and try again.');
        });
    } else {
      // If credentials exist, update existing credentials
      axios.put(`${process.env.NEXT_PUBLIC_BACKEND}/update_credentials`, updatedJanData, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then(response => {
          setJanMessage(response.data.message);
          setJanErrorMessage('');
          // Update janCred state or variable here if needed
        })
        .catch(error => {
          setJanErrorMessage(error.response && error.response.data.message
            ? error.response.data.message
            : 'Update failed. Please check your input and try again.');
        });
    }
  };

  const handleChange = (name, value) => {
    setJanData(prevJanData => ({
      ...prevJanData,
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
    <div className="container mx-auto px-4">
      <h1 className='my-4'>Settings</h1>
      <div className="flex justify-between">
        {/* Left Column: Account Information */}
        <div className="w-full max-w px-4">
          <form onSubmit={handleSubmitAccount}>
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
                        onChange={(e) => setFormData(prevFormData => ({
                          ...prevFormData,
                          [key]: e.target.value
                        }))}
                      />
                    </div>
                  ))}
                </div>
              )}
              <Button className="button-text w-full" type="submit" color="primary" auto>
                Update Account
              </Button>
              {(accountErrorMessage && (
                <p className="text-center text-sm text-red-600 mt-1">{accountErrorMessage}</p>
              )) ||
              (accountMessage && (
                <p className="text-center text-sm text-green-600 mt-1">{accountMessage}</p>
              ))}
            </div>
          </form>
        </div>

        {/* Right Column: JAN Credentials */}
        <div className="w-full max-w px-4">
          <form onSubmit={handleSubmitJan}>
            <h2 className='mb-2'>Jan.ai Credentials</h2>
            <div className="grid grid-cols-1 gap-y-2">
              {userData && (
                <div>
                  <div className="group relative mb-2">
                    <Input
                      size="md"
                      type="text"
                      label="Jan.ai IP"
                      placeholder="Enter Jan.ai IP"
                      value={janData.jan_ip}
                      onChange={(e) => handleChange('jan_ip', e.target.value)}
                    />
                  </div>
                  <div className="group relative mb-2">
                    <Input
                      size="md"
                      type="text"
                      label="Jan.ai Port"
                      placeholder="Enter Jan.ai Port"
                      value={janData.jan_port}
                      onChange={(e) => handleChange('jan_port', e.target.value)}
                    />
                  </div>
                  <div className="group relative mb-2">
                    <Input
                      size="md"
                      type="text"
                      label="Jan.ai Prefix"
                      placeholder="Enter Jan.ai Prefix"
                      value={janData.jan_prefix}
                      onChange={(e) => handleChange('jan_prefix', e.target.value)}
                    />
                  </div>
                  <Button className="button-text w-full" type="submit" color="primary" auto>
                    Update Jan
                  </Button>
                  {(janErrorMessage && (
                    <p className="text-center text-sm text-red-600 mt-1">{janErrorMessage}</p>
                  )) ||
                  (janMessage && (
                    <p className="text-center text-sm text-green-600 mt-1">{janMessage}</p>
                  ))}
                </div>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
