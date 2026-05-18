import './globals.css'
import type { ReactNode } from 'react'
import { Inria_Sans } from 'next/font/google'
import { AppToaster } from '@/components/ui/sooner'

const inriaSans = Inria_Sans({
  subsets: ['latin'],
  weight: ['400', '700'],
  style: ['normal', 'italic'],
  display: 'swap',
  variable: '--font-inria-sans',
})

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="cs">
      <body className={`${inriaSans.variable} font-sans`}>
        {children}
        <AppToaster />
      </body>
    </html>
  )
}