'use client';

export default function ChallengeCard({ challenge, showSubmitButton = true, onSubmit }) {
    const difficultyClass = `badge--${challenge.difficulty}`;

    return (
        <div className={`card ${challenge.user_submitted ? '' : 'card--highlight'}`}>
            <div className="flex flex-between mb-md">
                <span className={`badge ${difficultyClass}`}>
                    {challenge.difficulty.toUpperCase()}
                </span>
                <span className="badge badge--category">
                    {challenge.category.toUpperCase()}
                </span>
            </div>

            <h2 className="card__title">{challenge.title}</h2>

            <div className="challenge-content">
                {challenge.description}
            </div>

            <div className="flex flex-between mt-lg" style={{ alignItems: 'center' }}>
                <div>
                    <strong>POINTS:</strong> {challenge.points}
                </div>

                {challenge.user_submitted ? (
                    <span className="badge badge--easy">✓ SUBMITTED</span>
                ) : (
                    showSubmitButton && (
                        <button className="btn btn--primary" onClick={onSubmit}>
                            SUBMIT ANSWER
                        </button>
                    )
                )}
            </div>

            {challenge.expected_output && (
                <div className="mt-md" style={{ fontSize: '0.875rem', color: 'var(--fg-secondary)' }}>
                    <strong>EXPECTED:</strong> {challenge.expected_output}
                </div>
            )}
        </div>
    );
}
