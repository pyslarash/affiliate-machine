/** @type {import('next').NextConfig} */

import './env-config.js'; // Import the file that loads environment variables

const nextConfig = {
  env: {
    BACKEND: process.env.BACKEND,
  },
};

export default {
  ...nextConfig,
  async rewrites() {
    return [
      {
        source: '/:path*',
        destination: `${process.env.BACKEND}/:path*`, // Adjust the destination URL as needed
      },
    ];
  },
};