'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { register, login } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';

export default function RegisterPage() {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const router = useRouter();
    const { refreshUser } = useAuth();

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError('');

        if (password !== confirmPassword) {
            setError('PASSWORDS DO NOT MATCH');
            setLoading(false);
            return;
        }

        if (password.length < 6) {
            setError('PASSWORD MUST BE AT LEAST 6 CHARACTERS');
            setLoading(false);
            return;
        }

        try {
            await register(username, email, password);
            // Auto-login after registration
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
            <h1 className="text-center">REGISTER</h1>
            <p className="text-center mb-xl" style={{ color: 'var(--fg-secondary)' }}>
                COMMIT TO DAILY IMPROVEMENT
            </p>

            {error && (
                <div className="alert alert--error">
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="username">USERNAME</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        placeholder="your_username"
                        pattern="^[a-zA-Z0-9_]+$"
                        minLength={3}
                        maxLength={50}
                    />
                    <small style={{ color: 'var(--fg-secondary)' }}>
                        Letters, numbers, underscores only
                    </small>
                </div>

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
                        minLength={6}
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="confirmPassword">CONFIRM PASSWORD</label>
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        placeholder="••••••••"
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn--primary btn--block btn--large"
                    disabled={loading}
                >
                    {loading ? 'CREATING ACCOUNT...' : 'CREATE ACCOUNT'}
                </button>
            </form>

            <p className="text-center mt-xl">
                ALREADY HAVE AN ACCOUNT? <Link href="/login">LOGIN</Link>
            </p>
        </div>
    );
}
