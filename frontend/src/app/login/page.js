'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { login } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const { refreshUser } = useAuth();

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await login(email, password);
            await refreshUser();
            router.push('/challenge');
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="container container--narrow" style={{ paddingTop: 'var(--space-xxl)' }}>
            <h1 className="text-center">LOGIN</h1>
            <p className="text-center mb-xl" style={{ color: 'var(--fg-secondary)' }}>
                PROVE YOU'RE NOT A QUITTER
            </p>

            {error && (
                <div className="alert alert--error">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="email">EMAIL</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        placeholder="your@email.com"
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="password">PASSWORD</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        placeholder="••••••••"
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn--primary btn--block btn--large"
                    disabled={loading}
                >
                    {loading ? 'LOGGING IN...' : 'LOGIN'}
                </button>
            </form>

            <p className="text-center mt-xl">
                NO ACCOUNT? <Link href="/register">REGISTER NOW</Link>
            </p>
        </div>
    );
}
