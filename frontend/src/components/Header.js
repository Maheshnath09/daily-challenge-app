'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

export default function Header() {
    const { user, logout, isAuthenticated } = useAuth();
    const router = useRouter();
    const [menuOpen, setMenuOpen] = useState(false);

    function handleLogout() {
        logout();
        router.push('/login');
        setMenuOpen(false);
    }

    function toggleMenu() {
        setMenuOpen(!menuOpen);
    }

    function closeMenu() {
        setMenuOpen(false);
    }

    return (
        <header className="header">
            <div className="header__inner">
                <Link href={isAuthenticated ? '/challenge' : '/'} className="header__logo" onClick={closeMenu}>
                    DAILY<span style={{ color: 'var(--accent)' }}>_</span>CHALLENGE
                </Link>

                <button className="mobile-menu-btn" onClick={toggleMenu} aria-label="Toggle menu">
                    {menuOpen ? '✕' : '☰'}
                </button>

                {isAuthenticated ? (
                    <nav className={`header__nav ${menuOpen ? 'active' : ''}`}>
                        <Link href="/challenge" onClick={closeMenu}>TODAY</Link>
                        <Link href="/leaderboard" onClick={closeMenu}>RANK</Link>
                        <Link href="/profile" onClick={closeMenu}>PROFILE</Link>
                        <button
                            onClick={handleLogout}
                            className="btn"
                            style={{ padding: '8px 16px', fontSize: '0.875rem' }}
                        >
                            LOGOUT
                        </button>
                    </nav>
                ) : (
                    <nav className={`header__nav ${menuOpen ? 'active' : ''}`}>
                        <Link href="/login" onClick={closeMenu}>LOGIN</Link>
                        <Link href="/register" onClick={closeMenu}>REGISTER</Link>
                    </nav>
                )}
            </div>
        </header>
    );
}

