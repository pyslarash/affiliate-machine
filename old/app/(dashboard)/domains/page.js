'use client'

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Oswald } from 'next/font/google';

const oswald = Oswald({
  display: 'swap',
  subsets: ['latin'],
  weight: '600'
});

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
    <div>
      <div>
        <h1 className={`${oswald.className} page-header`}>Domains</h1>
        {/* Add your dashboard content here */}
      </div>
    </div>
  );
}