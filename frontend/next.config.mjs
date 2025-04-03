import { withPayload } from '@payloadcms/next/withPayload'

/** @type {import('next').NextConfig} */
const nextConfig = {
  assetPrefix: '/edupo-coolify',
  // basePath: '/edupo-coolify'
  // Your Next.js config here
}

export default withPayload(nextConfig)
