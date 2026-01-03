'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { getTodayChallenge } from '@/lib/api';
import ChallengeCard from '@/components/ChallengeCard';
import SubmitForm from '@/components/SubmitForm';
import Countdown from '@/components/Countdown';

export default function ChallengePage() {
    const { user, isAuthenticated, loading: authLoading, refreshUser } = useAuth();
    const [challenge, setChallenge] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [showSubmitForm, setShowSubmitForm] = useState(false);
    const [submissionSuccess, setSubmissionSuccess] = useState(null);
    const router = useRouter();

    useEffect(() => {
        if (!authLoading && !isAuthenticated) {
            router.push('/login');
            return;
        }

        if (isAuthenticated) {
            fetchChallenge();
        }
    }, [isAuthenticated, authLoading, router]);

    async function fetchChallenge() {
        try {
            const data = await getTodayChallenge();
            setChallenge(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    function handleSubmitClick() {
        setShowSubmitForm(true);
    }

    async function handleSubmissionSuccess(submission) {
        setSubmissionSuccess(submission);
        setShowSubmitForm(false);
        // Refresh challenge to show submitted state
        await fetchChallenge();
        // Refresh user to update streak/points
        await refreshUser();
    }

    if (authLoading || loading) {
        return <div className="loading">LOADING CHALLENGE...</div>;
    }

    if (error) {
        return (
            <div className="container" style={{ paddingTop: 'var(--space-xxl)' }}>
                <div className="alert alert--error">
                    {error}
                </div>
                <p className="text-center mt-lg">
                    No challenge available today. Check back tomorrow at 00:00 UTC.
                </p>
            </div>
        );
    }

    return (
        <div className="container" style={{ paddingTop: 'var(--space-xl)' }}>
            <Countdown />

            {user && (
                <div className="flex flex-between mb-lg" style={{ alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
                    <div>
                        <span style={{ color: 'var(--fg-secondary)' }}>STREAK:</span>{' '}
                        <strong style={{ fontSize: '1.5rem' }}>
                            {user.current_streak > 0 && '🔥'} {user.current_streak}
                        </strong>
                    </div>
                    <div>
                        <span style={{ color: 'var(--fg-secondary)' }}>POINTS:</span>{' '}
                        <strong style={{ fontSize: '1.5rem' }}>{user.total_points}</strong>
                    </div>
                </div>
            )}

            {submissionSuccess && (
                <div className="alert alert--success mb-lg">
                    <strong>✓ SUBMITTED!</strong> You earned {submissionSuccess.points_awarded} points.
                    {user && user.current_streak >= 7 && ' (Includes streak bonus!)'}
                </div>
            )}

            {challenge && (
                <>
                    <ChallengeCard
                        challenge={challenge}
                        onSubmit={handleSubmitClick}
                        showSubmitButton={!showSubmitForm && !challenge.user_submitted}
                    />

                    {showSubmitForm && !challenge.user_submitted && (
                        <div className="card mt-lg">
                            <SubmitForm
                                challenge={challenge}
                                onSuccess={handleSubmissionSuccess}
                            />
                            <button
                                className="btn btn--block mt-md"
                                onClick={() => setShowSubmitForm(false)}
                            >
                                CANCEL
                            </button>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}
