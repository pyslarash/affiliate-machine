'use client'

import { useEffect, useState } from "react"
import { useTheme } from "next-themes"
import { Switch } from "@nextui-org/react";
import { SunIcon } from '@heroicons/react/24/outline'
import { MoonIcon } from '@heroicons/react/24/outline'

export default function ThemeSwitcher() {
    const [mounted, setMounted] = useState(false);
    const { theme, setTheme, resolvedTheme } = useTheme();  // Using resolvedTheme to handle system preferences

    useEffect(() => {
        setMounted(true);
    }, []);

    if (!mounted) return null;

    // Function to toggle themes
    const toggleTheme = () => {
        setTheme(theme === 'dark' || resolvedTheme === 'dark' ? 'light' : 'dark');
    };

    return (
        <div className="flex gap-4">
            <Switch
                checked={theme === 'dark' || resolvedTheme === 'dark'}
                onChange={toggleTheme}
                size="lg"
                color="primary"
                startContent={<SunIcon />}
                endContent={<MoonIcon />}
            >
            </Switch>
        </div>
    );
}