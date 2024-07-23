// Import React
'use client'

import React from 'react';
import Link from 'next/link';
import Gear from './Gear';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { Lobster } from 'next/font/google';

const lobster = Lobster({
    display: 'swap',
    subsets: ['latin'],
    weight: '400'
});

const menuItems = [
    { path: "/dashboard", name: "Dashboard" },
    { path: "/domains", name: "Domains" },
    { path: "/processeddomains", name: "Processed Domains" },
    { path: "/websites", name: "Websites" },
    { path: "/wpautomation", name: "Wordpress Automation" },
    { path: "/keywords", name: "Keywords" },
    { path: "/article", name: "Article Writer" },
    { path: "/settings", name: "Settings" }
];

const MemoizedGear = React.memo(Gear);

const Sidebar = () => {
    const router = useRouter();

    const handleLogout = () => {
        const token = localStorage.getItem('token');
        if (!token) {
            console.error('Token not found in localStorage');
            return;
        }

        const config = {
            headers: {
                Authorization: `Bearer ${token}`
            }
        };

        const userId = localStorage.getItem('user_id');
        if (!userId) {
            console.error('User ID not found in localStorage');
            return;
        }

        axios.post(`${process.env.BACKEND}/logout_user/${userId}`, null, config)
            .then(response => {
                localStorage.removeItem('token');
                localStorage.removeItem('expiration_time');
                localStorage.removeItem('user_id');
                router.push('/login');
            })
            .catch(error => {
                console.error('Logout failed:', error);
            });
    };

    return (
        <div className="min-h-screen flex flex-col">
            <div className="flex flex-col md:flex-row flex-1">
                <aside className="sidebar w-full md:w-60">
                    <MemoizedGear small={true} /> {/* Wrap the Gear component with React.memo */}
                    <h1 className={`${lobster.className} logo-sidebar mb-6`}>Affiliate Machine</h1>
                    <ul className="mt-4">
                        {menuItems.map((item, index) => (
                            <li className="sidebar-menu-item" key={index}>
                                <Link href={item.path}>
                                    <span className="menu-text">{item.name}</span>
                                </Link>
                            </li>
                        ))}
                    </ul>
                    <div className="absolute bottom-4 left-0 right-0 mb-4 flex justify-center">
                        <button className="logout-button" onClick={handleLogout}>Logout</button>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default Sidebar;
