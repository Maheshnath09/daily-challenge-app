'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { getLeaderboard } from '@/lib/api';
import LeaderboardTable from '@/components/LeaderboardTable';

export default function LeaderboardPage() {
    const { user } = useAuth();
    const [leaderboard, setLeaderboard] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchLeaderboard();
    }, []);

    async function fetchLeaderboard() {
        try {
            const data = await getLeaderboard(50);
            setLeaderboard(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return <div className="loading">LOADING RANKINGS...</div>;
    }

    return (
        <div className="container" style={{ paddingTop: 'var(--space-xl)' }}>
            <h1 className="text-center">LEADERBOARD</h1>
            <p className="text-center mb-xl" style={{ color: 'var(--fg-secondary)' }}>
                TOP 50 CHALLENGERS
            </p>

            {error && (
                <div className="alert alert--error">
                    {error}
                </div>
            )}

            {leaderboard.length === 0 ? (
                <div className="card text-center">
                    <h3>NO RANKINGS YET</h3>
                    <p>Be the first to complete a challenge!</p>
                </div>
            ) : (
                <LeaderboardTable
                    users={leaderboard}
                    currentUserId={user?.id}
                />
            )}

            <div className="mt-xl text-center" style={{ color: 'var(--fg-secondary)' }}>
                <p>RANKED BY TOTAL POINTS, THEN STREAK</p>
            </div>
        </div>
    );
}
