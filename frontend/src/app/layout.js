'use client'

import './globals.css';
import { Lexend, Montserrat } from 'next/font/google';
import TopBar from './components/Navbar';
import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

export const lexend = Lexend({
  subsets: ['latin'],
  display: 'swap',
})

export const montserrat = Montserrat({
  subsets: ['latin'],
  display: 'swap',
})

export default function RootLayout({ children }) {
  console.log("Loading the layout")
  return (
    <html lang="en">
      <body className={`${lexend.className} ${montserrat.className}`}>
        <NextUIProvider>
          <NextThemesProvider attribute="class" defaultTheme="light">
            <header className='py-6'>
              <TopBar />
            </header>
            <main>{children}</main>
            <footer></footer>
          </NextThemesProvider>
        </NextUIProvider>
      </body>
    </html>
  )
}
