'use client'

import { useEffect, useState } from 'react'
import { DesktopSplashScreen } from './splash/desktop-splash-screen'
import { MobileSplashScreen } from './splash/mobile-splash-screen'

export function SplashScreen() {
  const [isVisible, setIsVisible] = useState(true)
  const [isFading, setIsFading] = useState(false)

  useEffect(() => {
    const fadeTimer = window.setTimeout(() => {
      setIsFading(true)
    }, 2000)

    const hideTimer = window.setTimeout(() => {
      setIsVisible(false)
    }, 2300)

    return () => {
      window.clearTimeout(fadeTimer)
      window.clearTimeout(hideTimer)
    }
  }, [])

  if (!isVisible) return null

  return (
    <>
      <div className="block desktop:hidden">
        <MobileSplashScreen isFading={isFading} />
      </div>
      <div className="hidden desktop:block">
        <DesktopSplashScreen isFading={isFading} />
      </div>
    </>
  )
}