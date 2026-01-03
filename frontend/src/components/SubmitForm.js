'use client';

import { useState } from 'react';
import { submitChallenge } from '@/lib/api';

export default function SubmitForm({ challenge, onSuccess }) {
    const [content, setContent] = useState('');
    const [submissionType, setSubmissionType] = useState(
        challenge.category === 'life' ? 'checkbox' : 'text'
    );
    const [completed, setCompleted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            // For life challenges, just mark as completed
            const submissionContent = submissionType === 'checkbox' ? 'Completed' : content;
            const isCompleted = submissionType === 'checkbox' ? completed : true;

            if (submissionType === 'checkbox' && !completed) {
                setError('You must mark the challenge as completed');
                setLoading(false);
                return;
            }

            if (submissionType !== 'checkbox' && !content.trim()) {
                setError('Please provide your answer');
                setLoading(false);
                return;
            }

            const result = await submitChallenge(
                challenge.id,
                submissionContent,
                submissionType,
                isCompleted
            );

            if (onSuccess) {
                onSuccess(result);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h3 className="mb-lg">SUBMIT YOUR ANSWER</h3>

            {error && (
                <div className="alert alert--error mb-lg">
                    {error}
                </div>
            )}

            {challenge.category === 'life' ? (
                <div className="form-group">
                    <label style={{ display: 'flex', alignItems: 'center', gap: '16px', cursor: 'pointer' }}>
                        <input
                            type="checkbox"
                            checked={completed}
                            onChange={(e) => setCompleted(e.target.checked)}
                            style={{
                                width: '32px',
                                height: '32px',
                                cursor: 'pointer',
                                accentColor: 'var(--accent)'
                            }}
                        />
                        <span style={{ fontSize: '1.25rem' }}>
                            I COMPLETED THIS CHALLENGE. I AM NOT LYING.
                        </span>
                    </label>
                </div>
            ) : (
                <>
                    <div className="form-group">
                        <label htmlFor="submissionType">SUBMISSION TYPE</label>
                        <select
                            id="submissionType"
                            value={submissionType}
                            onChange={(e) => setSubmissionType(e.target.value)}
                        >
                            <option value="text">TEXT</option>
                            <option value="code">CODE</option>
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="content">
                            YOUR {submissionType === 'code' ? 'CODE' : 'ANSWER'}
                        </label>
                        <textarea
                            id="content"
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            rows={submissionType === 'code' ? 15 : 8}
                            placeholder={
                                submissionType === 'code'
                                    ? 'Paste your code here...'
                                    : 'Enter your answer...'
                            }
                            style={{
                                fontFamily: submissionType === 'code' ? 'monospace' : 'inherit',
                                resize: 'vertical'
                            }}
                        />
                    </div>
                </>
            )}

            <button
                type="submit"
                className="btn btn--primary btn--large btn--block"
                disabled={loading}
            >
                {loading ? 'SUBMITTING...' : 'SUBMIT'}
            </button>

            <p className="mt-md text-center" style={{ color: 'var(--fg-secondary)', fontSize: '0.875rem' }}>
                ⚠️ YOU CAN ONLY SUBMIT ONCE. NO TAKE-BACKS.
            </p>
        </form>
    );
}
