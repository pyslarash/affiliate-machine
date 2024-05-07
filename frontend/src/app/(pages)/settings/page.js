'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Oswald } from 'next/font/google';
import axios from 'axios';

const oswald = Oswald({
  display: 'swap',
  subsets: ['latin'],
  weight: '600'
});

export default function Settings() {
  const router = useRouter();
  const [userData, setUserData] = useState(null);
  const [message, setMessage] = useState('');
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
      axios.get(`${process.env.BACKEND}/get_user/${userID}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        setUserData(response.data);
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

    console.log('Submitting:', formData);  // Add this to log form data

    axios.put(`${process.env.BACKEND}/edit_user/${userID}`, formData, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then(response => {
      console.log('User information updated:', response.data);
      setMessage(response.data.message);
    })
    .catch(error => {
      console.error('Error updating user information:', error);
      setMessage(error.response.data.message || 'Failed to update user information');
    });
};

  const handleChange = (e) => {
    const { name, value } = e.target;
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
    <div>
      {/* Main Header */}
      <h1 className={`${oswald.className} page-header`}>Settings</h1>
      {/* Main Table */}
      {/* Account Update Form */}
      <form onSubmit={handleSubmit}>
      <h2 className={`${oswald.className} sub-header ml-7 mb-2`}>Account</h2>   
      <div className="mx-auto ml-7 grid grid-cols-1">
      
        {userData && (
          <div>
            {Object.keys(formData).map((key, index) => (
              <div className="group relative mb-2" key={index}>
                <div className="settings-font">
                  {key === 'password' ? 'Password:' : `${formatLabel(key)}:`}
                </div>
                <input
                  className="input-field"
                  placeholder={`Change ${formatLabel(key)}`}
                  type={key === 'password' ? 'password' : 'text'}
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                />
              </div>
            ))}
          </div>
        )}
        <button type="submit" className="login-button col-span-2">Update</button>
        {message && <span className="message mt-3">{message}</span>}
      </div>
    </form>
    <div>

    </div>
  </div>
  );
}
