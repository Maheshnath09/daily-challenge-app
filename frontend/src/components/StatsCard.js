'use client';

export default function StatsCard({ label, value, icon }) {
    return (
        <div className="stat">
            {icon && <div style={{ fontSize: '2rem', marginBottom: '8px' }}>{icon}</div>}
            <div className="stat__value">{value}</div>
            <div className="stat__label">{label}</div>
        </div>
    );
}
