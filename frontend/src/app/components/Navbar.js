'use client'

import React from "react";
import { useState } from "react";
import { Navbar, NavbarBrand, NavbarContent, NavbarItem, NavbarMenuToggle, NavbarMenu, NavbarMenuItem, Link, Button } from "@nextui-org/react";
import ThemeSwitcher from "./ThemeSwtcher";
import Gear from "./Gear";

export default function TopBar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const currentPath = typeof window !== 'undefined' ? window.location.pathname : '';
  const isLoggedIn = /* Your logic to determine if the user is logged in */ false;

  const menuItems = [
    "Dashboard",
    "Domains",
    "Websites",
    "Keywords",
    "Posts",
    "Settings"
  ];

  return (
    <Navbar onMenuOpenChange={setIsMenuOpen}>
      <NavbarContent>
        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="sm:hidden"
        />
        <NavbarBrand className="md:justify-self-center">
          <Link color="foreground" href="/">
            <Gear />
            <p className="font-bold text-inherit">aMachine</p>
          </Link>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-6" justify="center">
        <NavbarItem>
          <Link color="foreground" href="#">
            Features
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="#" aria-current="page">
            Customers
          </Link>
        </NavbarItem>
        <NavbarItem>
          <Link color="foreground" href="#">
            Integrations
          </Link>
        </NavbarItem>
      </NavbarContent>
      <NavbarContent justify="end">
        {currentPath === "/" && !isLoggedIn && (
          <NavbarItem>
            <Button as={Link} color="primary" href="#" variant="flat">
              <Link href="/login">Login</Link>
            </Button>
          </NavbarItem>
        )}
        {isLoggedIn && (
          <>
            <NavbarItem className="hidden lg:flex">
              <Link href="/logout">Logout</Link>
            </NavbarItem>
          </>
        )}
      </NavbarContent>
      <NavbarMenu>
        {menuItems.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              color={
                index === 2 ? "primary" : index === menuItems.length - 1 ? "danger" : "foreground"
              }
              className="w-full"
              href="#"
              size="lg"
            >
              {item}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
      <ThemeSwitcher />
    </Navbar>
  );
}