'use client';

import { createContext, useContext, useState, useEffect } from 'react';
import { getCurrentUser, logout as apiLogout, isAuthenticated } from '@/lib/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    async function checkAuth() {
        if (isAuthenticated()) {
            try {
                const userData = await getCurrentUser();
                setUser(userData);
            } catch (error) {
                console.error('Auth check failed:', error);
                apiLogout();
                setUser(null);
            }
        }
        setLoading(false);
    }

    async function refreshUser() {
        if (isAuthenticated()) {
            try {
                const userData = await getCurrentUser();
                setUser(userData);
            } catch (error) {
                console.error('Failed to refresh user:', error);
            }
        }
    }

    function logout() {
        apiLogout();
        setUser(null);
    }

    const value = {
        user,
        setUser,
        loading,
        logout,
        refreshUser,
        isAuthenticated: !!user,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}
