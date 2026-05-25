'use client'

import Image from 'next/image'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { FullscreenBrandScreen } from '@/components/layout/mobile/fullscreen-brand-screen'

const WELCOME_SEEN_KEY = 'edupo-welcome-seen'

export function WelcomeScreen() {
  const router = useRouter()

  useEffect(() => {
    const alreadySeen = window.localStorage.getItem(WELCOME_SEEN_KEY)

    if (alreadySeen === 'true') {
      router.replace('/dashboard')
    }
  }, [router])

  function handleContinue() {
    window.localStorage.setItem(WELCOME_SEEN_KEY, 'true')
    router.push('/dashboard')
  }

  return (
    <FullscreenBrandScreen>
      <section className="flex grow flex-col items-center justify-between text-center">
        <p className="typo-h3 max-w-83">
          Vytvořte si svou jedinečnou báseň
        </p>
        <Image
          src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/girl-with-computer.svg"}
          alt=""
          width={280}
          height={240}
          style={{ width: '280px', height: '240px' }}
          priority
        />
        <p className="typo-large max-w-83">
          Nastavte autora, styl a motivy podle svých představ. AI vytvoří báseň přesně pro vás.
        </p>
        <Button
          variant="subtle"
          size="md"
          onClick={handleContinue}
        >
          Pokračovat
        </Button>
      </section>
    </FullscreenBrandScreen>

  )
}