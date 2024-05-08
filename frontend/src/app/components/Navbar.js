import React, { useState } from "react";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, Link, Button } from "@nextui-org/react";
import { useRouter } from 'next/navigation';
import axios from 'axios';
import ThemeSwitcher from "./ThemeSwtcher";
import Gear from "./Gear";
import { useAuth } from "../authContext";

export default function TopBar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const router = useRouter();
  const { isLoggedIn, setIsLoggedIn } = useAuth(); // Retrieve global login state

  // Handle the logout process
  const handleLogout = async () => {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('token');
    if (!userId) return;

    try {
      // Make the POST request to the logout endpoint
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND}/logout_user/${userId}`,
        {}, // No body needed for this request
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      console.log('Logout Response:', response);

      // Clear local storage items
      localStorage.removeItem('token');
      localStorage.removeItem('expiration_time');
      localStorage.removeItem('user_id');

      // Update global login state and navigate to the login page
      setIsLoggedIn(false);
      router.push('/login');
    } catch (error) {
      console.log('Error during logout:', error);
    }
  };

  // Menu items structured as "name": "path"
  const menuItems = [
    { name: "Dashboard", path: "/dashboard" },
    { name: "Domains", path: "/domains" },
    { name: "Websites", path: "/websites" },
    { name: "Keywords", path: "/keywords" },
    { name: "Posts", path: "/posts" },
    { name: "Settings", path: "/settings" }
  ];

  return (
    <Navbar onMenuOpenChange={setIsMenuOpen} maxWidth="2xl">
      {/* Navbar Content */}
      <NavbarContent className="flex justify-between items-center">
      {isLoggedIn && (
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="sm:hidden"
        />
      )}
        <NavbarBrand>
          <Link color="foreground" href="/">
            <Gear />
            <p className="font-bold text-inherit">aMachine</p>
          </Link>
        </NavbarBrand>
      </NavbarContent>

      {/* Menu items visible on large screens */}
      {isLoggedIn && (
        <NavbarContent className="hidden sm:flex gap-6" justify="center">
          {menuItems.map(({ name, path }, index) => (
            <NavbarItem key={index}>
              <Link color="foreground" href={path}>
                {name}
              </Link>
            </NavbarItem>
          ))}
        </NavbarContent>
      )}
      {/* Login/Logout Buttons */}
      <NavbarContent justify="end">
        {isLoggedIn ? (
          <NavbarItem className="hidden lg:flex">
            <Button color="primary" variant="flat" onPress={handleLogout}>
              Log Out
            </Button>
          </NavbarItem>
        ) : (
          <NavbarItem>
            <Button as={Link} color="primary" href="/login" variant="flat">
              Login
            </Button>
          </NavbarItem>
        )}
      </NavbarContent>

      {/* Dropdown menu for small screens */}
      
      {isLoggedIn && (
        <NavbarMenu className="mt-3">
          {menuItems.map(({ name, path }, index) => (
            <NavbarMenuItem key={index}>
              <Link
                color="foreground"
                className="w-full"
                href={path}
                size="lg"
              >
                {name}
              </Link>
            </NavbarMenuItem>
          ))}
          <NavbarMenuItem>
            <Link color="danger" className="w-full" onPress={handleLogout} size="lg">
              Log Out
            </Link>
          </NavbarMenuItem>
        </NavbarMenu>
      )}
      <ThemeSwitcher />
    </Navbar>
  );
}
