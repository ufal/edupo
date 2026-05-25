'use client'

import Image from 'next/image'
import { useEffect, useState } from 'react'
import { MobileHeader } from '@/components/layout/mobile/mobile-header'
import { MobileFullscreenOverlay } from './mobile-fullscreen-overlay'

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
    <MobileFullscreenOverlay className="z-[100]">
      <div
        className={[
          'flex h-full flex-col',
          'transition-opacity duration-300',
          isFading ? 'opacity-0' : 'opacity-100',
        ].join(' ')}
      >
        <MobileHeader mode="logo-only" />

        <section className="flex grow flex-col items-center justify-between gap-16 pt-10 pb-24">
          <Image src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/logos/logo-tacr.svg"} alt="TA ČR" width={38} height={38} priority />
          <Image src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/logos/logo-ucl.svg"} alt="Ústav české literatury AV ČR" width={116} height={54} priority />
          <Image src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/logos/logo-vsvu.svg"} alt="VŠVU Bratislava" width={102} height={41} priority />
          <Image src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/logos/logo-didaktikon.svg"} alt="Didaktikon" width={60} height={60} priority />
          <Image src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/logos/logo-matfyz.svg"} alt="Matfyz" width={87} height={38} priority />
        </section>
      </div>
    </MobileFullscreenOverlay>
  )
}