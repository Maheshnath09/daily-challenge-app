'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import StatsCard from '@/components/StatsCard';

export default function ProfilePage() {
    const { user, isAuthenticated, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && !isAuthenticated) {
            router.push('/login');
        }
    }, [isAuthenticated, loading, router]);

    if (loading) {
        return <div className="loading">LOADING PROFILE...</div>;
    }

    if (!user) {
        return null;
    }

    const joinDate = new Date(user.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    return (
        <div className="container" style={{ paddingTop: 'var(--space-xl)' }}>
            <h1 className="text-center">{user.username.toUpperCase()}</h1>
            <p className="text-center mb-xl" style={{ color: 'var(--fg-secondary)' }}>
                {user.email}
            </p>

            <div className="grid grid--2 mb-xl">
                <StatsCard
                    icon="🔥"
                    value={user.current_streak}
                    label="Current Streak"
                />
                <StatsCard
                    icon="👑"
                    value={user.longest_streak}
                    label="Longest Streak"
                />
                <StatsCard
                    icon="⚡"
                    value={user.total_points}
                    label="Total Points"
                />
                <StatsCard
                    icon="🏆"
                    value={`#${user.rank || '—'}`}
                    label="Global Rank"
                />
            </div>

            <div className="card">
                <h3>ACCOUNT DETAILS</h3>
                <div style={{ marginTop: 'var(--space-md)' }}>
                    <p>
                        <strong>USERNAME:</strong> {user.username}
                    </p>
                    <p>
                        <strong>EMAIL:</strong> {user.email}
                    </p>
                    <p>
                        <strong>JOINED:</strong> {joinDate}
                    </p>
                    <p>
                        <strong>TOTAL SUBMISSIONS:</strong> {user.total_submissions}
                    </p>
                    {user.last_completed_date && (
                        <p>
                            <strong>LAST COMPLETED:</strong>{' '}
                            {new Date(user.last_completed_date).toLocaleDateString()}
                        </p>
                    )}
                </div>
            </div>

            <div className="card mt-lg" style={{ borderColor: 'var(--accent)' }}>
                <h3>STREAK RULES</h3>
                <ul style={{ paddingLeft: 'var(--space-lg)', marginTop: 'var(--space-md)' }}>
                    <li>Complete today's challenge before midnight UTC</li>
                    <li>Skip a day = streak resets to zero</li>
                    <li>Longest streak is preserved forever</li>
                    <li>7+ day streak = +5 bonus points per challenge</li>
                </ul>
            </div>
        </div>
    );
}
