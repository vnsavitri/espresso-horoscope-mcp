import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  // Use port 3001 to avoid conflicts with other services
  server: {
    port: 3001,
  },
};

export default nextConfig;
