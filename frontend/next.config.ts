import type { NextConfig } from 'next';
const config: NextConfig = {
  output:
    process.env.BALNLP_STATIC_EXPORT === '1'
      ? 'export'
      : process.env.BALNLP_DOCKER_BUILD === '1'
        ? 'standalone'
        : undefined,
  poweredByHeader: false,
  trailingSlash: process.env.BALNLP_STATIC_EXPORT === '1',
  ...(process.env.BALNLP_STATIC_EXPORT === '1'
    ? {}
    : {
        async rewrites() {
          return [
            {
              source: '/api/v1/:path*',
              destination: `${process.env.API_PROXY_URL || 'http://127.0.0.1:8000'}/api/v1/:path*`,
            },
          ];
        },
      }),
  async headers() {
    if (process.env.BALNLP_STATIC_EXPORT === '1') return [];
    return [
      {
        source: '/(.*)',
        headers: [
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'no-referrer' },
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
    ];
  },
};
export default config;
