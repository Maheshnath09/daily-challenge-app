/**
 * API Client for Daily Challenge App
 * Handles all HTTP requests to the backend
 */

// Use Next.js API rewrites to proxy requests - this bypasses CORS
// OR use the environment variable if set (for production/local separation)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

/**
 * Get the stored auth token
 */
function getToken() {
    if (typeof window !== 'undefined') {
        return localStorage.getItem('token');
    }
    return null;
}

/**
 * Make an authenticated API request
 */
async function apiRequest(endpoint, options = {}) {
    const token = getToken();

    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
        throw new Error(error.detail || `HTTP error ${response.status}`);
    }

    return response.json();
}

// ===== AUTH API =====

export async function register(username, email, password) {
    return apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, email, password }),
    });
}

export async function login(email, password) {
    const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
    });

    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
    }

    return data;
}

export function logout() {
    localStorage.removeItem('token');
}

// ===== CHALLENGE API =====

export async function getTodayChallenge() {
    return apiRequest('/challenge/today');
}

export async function getChallengeHistory(page = 1, pageSize = 10) {
    return apiRequest(`/challenge/history?page=${page}&page_size=${pageSize}`);
}

export async function submitChallenge(challengeId, content, submissionType = 'text', completed = true) {
    return apiRequest('/challenge/submit', {
        method: 'POST',
        body: JSON.stringify({
            challenge_id: challengeId,
            content,
            submission_type: submissionType,
            completed,
        }),
    });
}

// ===== USER API =====

export async function getCurrentUser() {
    return apiRequest('/user/me');
}

export async function getLeaderboard(limit = 50) {
    return apiRequest(`/user/leaderboard?limit=${limit}`);
}

// ===== UTILS =====

export function isAuthenticated() {
    return !!getToken();
}
