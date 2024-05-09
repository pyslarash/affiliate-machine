// RootLayout component
'use client'

import { useState, useEffect, useMemo } from 'react';
import { usePathname } from 'next/navigation';
import './globals.css';
import { Lexend, Montserrat } from 'next/font/google';
import TopBar from './components/Navbar';
import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { AuthProvider } from './authContext';

export const lexend = Lexend({
  subsets: ['latin'],
  display: 'swap',
});

export const montserrat = Montserrat({
  subsets: ['latin'],
  display: 'swap',
});

export default function RootLayout({ children }) {
  const pathname = usePathname();
  const [isLoginPage, setIsLoginPage] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const memoizedPathname = useMemo(() => pathname, [pathname]);

  // Effect to check login state from localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userId = localStorage.getItem('user_id');
    if (token && userId) {
      setIsLoggedIn(true);
    }
  }, []);

  useEffect(() => {
    console.log(memoizedPathname);
    if (memoizedPathname === '/login') {
      setIsLoginPage(true);
    } else {
      setIsLoginPage(false);
    }
  }, [memoizedPathname]);

  // Determine the positioning style of the header based on the current page
  const headerStyle = isLoginPage ? { position: 'absolute' } : { position: 'relative' };

  return (
    <html lang="en">
      <body className={`${lexend.className} ${montserrat.className}`}>
        <AuthProvider>
          <NextUIProvider>
            <NextThemesProvider attribute="class" defaultTheme="light">
              <header style={headerStyle} className='justify-between inset-x-0 py-6'>
                <TopBar isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
              </header>
              <main>{children}</main>
              <footer></footer>
            </NextThemesProvider>
          </NextUIProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
