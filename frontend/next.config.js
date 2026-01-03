/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Use 'backend' hostname for Docker networking, fallback to localhost for local dev
        destination: process.env.NODE_ENV === 'production'
          ? 'http://backend:8000/:path*'
          : 'http://localhost:8000/:path*',
      },
    ];
  },
};

module.exports = nextConfig;

