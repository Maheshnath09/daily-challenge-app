'use client';

export default function LeaderboardTable({ users, currentUserId }) {
    return (
        <div style={{ overflowX: 'auto' }}>
            <table className="table">
                <thead>
                    <tr>
                        <th>RANK</th>
                        <th>USER</th>
                        <th>POINTS</th>
                        <th>STREAK</th>
                        <th>BEST</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr
                            key={user.id}
                            style={user.id === currentUserId ? {
                                backgroundColor: 'var(--accent)',
                                color: 'var(--fg-inverse)'
                            } : {}}
                        >
                            <td style={{ fontWeight: 'bold', fontSize: '1.25rem' }}>
                                #{user.rank}
                            </td>
                            <td>
                                {user.username}
                                {user.id === currentUserId && ' (YOU)'}
                            </td>
                            <td style={{ fontWeight: 'bold' }}>
                                {user.total_points}
                            </td>
                            <td>
                                {user.current_streak > 0 && '🔥'} {user.current_streak}
                            </td>
                            <td>
                                {user.longest_streak}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
