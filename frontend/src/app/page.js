'use client';

import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function Home() {
    const { isAuthenticated, loading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!loading && isAuthenticated) {
            router.push('/challenge');
        }
    }, [isAuthenticated, loading, router]);

    if (loading) {
        return <div className="loading">LOADING...</div>;
    }

    return (
        <>
            <section className="hero">
                <h1>
                    DAILY<span style={{ color: 'var(--accent)' }}>_</span>CHALLENGE
                </h1>
                <p className="hero__subtitle">
                    ONE CHALLENGE. EVERY DAY. NO EXCUSES.
                </p>
                <div className="flex gap-md mt-xl">
                    <Link href="/register" className="btn btn--primary btn--large">
                        START NOW
                    </Link>
                    <Link href="/login" className="btn btn--large">
                        LOGIN
                    </Link>
                </div>
            </section>

            <section className="container" style={{ paddingTop: 'var(--space-xxl)', paddingBottom: 'var(--space-xxl)' }}>
                <div className="grid grid--2">
                    <div className="card">
                        <h3>🎯 ONE CHALLENGE</h3>
                        <p>
                            Every day at midnight UTC, a new challenge drops.
                            Logic. Coding. Life. You choose nothing - we choose for you.
                        </p>
                    </div>

                    <div className="card">
                        <h3>🔥 BUILD STREAKS</h3>
                        <p>
                            Complete challenges daily to build your streak.
                            Skip a day? Streak dies. Simple as that.
                        </p>
                    </div>

                    <div className="card">
                        <h3>⚡ EARN POINTS</h3>
                        <p>
                            Easy = 10pts. Medium = 20pts. Hard = 30pts.
                            7+ day streak? Bonus +5 points per challenge.
                        </p>
                    </div>

                    <div className="card">
                        <h3>🏆 CLIMB RANKS</h3>
                        <p>
                            Global leaderboard. No hiding.
                            Your consistency is visible to everyone.
                        </p>
                    </div>
                </div>
            </section>

            <section style={{ backgroundColor: 'var(--fg-primary)', color: 'var(--fg-inverse)', padding: 'var(--space-xxl)' }}>
                <div className="container text-center">
                    <h2>STOP PROCRASTINATING</h2>
                    <p style={{ fontSize: '1.25rem', marginTop: 'var(--space-lg)', marginBottom: 'var(--space-xl)' }}>
                        Your future self is watching you right now through your memories.
                    </p>
                    <Link href="/register" className="btn btn--large" style={{ borderColor: 'var(--fg-inverse)', color: 'var(--fg-inverse)' }}>
                        ACCEPT THE CHALLENGE
                    </Link>
                </div>
            </section>

            <footer style={{ borderTop: 'var(--border-mega)', padding: 'var(--space-lg)', textAlign: 'center' }}>
                <p>DAILY CHALLENGE © {new Date().getFullYear()} | NO EXCUSES</p>
            </footer>
        </>
    );
}
