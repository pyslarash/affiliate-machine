'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const expirationTime = localStorage.getItem('expiration_time');
    const userID = localStorage.getItem('user_id');

    if (!token || !expirationTime || Date.now() > parseInt(expirationTime)) {
      // Token or expiration time is missing or token has expired
      redirectToLogin();
    }
  }, []);

  const redirectToLogin = () => {
    window.location.href = '/login';
  };

  return (
    <div className="flex justify-left">
      <div className="container mx-auto px-4">
        <h1 className='my-4'>Keywords</h1>
        {/* Add your dashboard content here */}
      </div>
    </div>
  );
}