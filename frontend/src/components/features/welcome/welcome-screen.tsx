'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { DesktopWelcomeScreen } from './desktop-welcome-screen'
import { MobileWelcomeScreen } from './mobile-welcome-screen'

const WELCOME_SEEN_KEY = 'edupo-welcome-seen'
const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

export function WelcomeScreen() {
  const router = useRouter()

  useEffect(() => {
    const alreadySeen = window.localStorage.getItem(WELCOME_SEEN_KEY)

    if (alreadySeen === 'true') {
      router.replace(`${base}dashboard`)
    }
  }, [router])

  function handleContinue() {
    window.localStorage.setItem(WELCOME_SEEN_KEY, 'true')
    router.push(`${base}dashboard`)
  }

  return (
    <>
      <div className="block desktop:hidden">
        <MobileWelcomeScreen onContinue={handleContinue} />
      </div>
      <div className="hidden desktop:block">
        <DesktopWelcomeScreen onContinue={handleContinue} />
      </div>
    </>
  )
}