// next.config.js
import path from "path";

/** @type {import('next').NextConfig} */
const nextConfig = {
  // Custom paths for our new structure
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "pixabay.com",
      },
      {
        protocol: "https",
        hostname: "cdn.pixabay.com",
      },
    ],
  },
  // Configure webpack for custom directories
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add aliases for easier imports
    config.resolve.alias = {
      ...config.resolve.alias,
      "@": path.resolve("."),
      "@/components": path.resolve("./components"),
      "@/shared": path.resolve("./shared"),
      "@/lib": path.resolve("./lib"),
      "@/hooks": path.resolve("./hooks"),
      "@/data": path.resolve("./data"),
    };

    return config;
  },
};

export default nextConfig;
