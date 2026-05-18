import { withPayload } from '@payloadcms/next/withPayload'

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  assetPrefix: '/edupo',
  // basePath: '/edupo-coolify'
  // Your Next.js config here
}

export default withPayload(nextConfig)
