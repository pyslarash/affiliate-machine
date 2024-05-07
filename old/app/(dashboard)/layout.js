import "../../app/globals.css"
import Sidebar from "../components/sidebar";
import { Lobster } from 'next/font/google';
import * as React from "react";
import {NextUIProvider} from "@nextui-org/react";

const lobster = Lobster({
    display: 'swap',
    subsets: ['latin'],
    weight: '400'
});

export const metadata = {
  title: "Affiliate Machine",
  description: "A place to manage your affiliate websites",
};

export default function RootLayout({ children }) {
  return (
    <NextUIProvider>
    <html lang="en">
      <head>
        {/* Include Lobster font */}
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <style>{lobster.styles}</style>
      </head>
      <body style={{ display: 'flex' }}>
        <Sidebar />
        <div>
          {children}
        </div>
      </body>
    </html>
    </NextUIProvider>
  );
}

