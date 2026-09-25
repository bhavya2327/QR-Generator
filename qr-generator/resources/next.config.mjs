/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/QR-Generator',
  trailingSlash: true,
  images: {
    unoptimized: true,
  }
};

export default nextConfig;
