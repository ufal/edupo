'use client'

import { Suspense, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

import { WelcomeScreen } from '@/components/features/welcome/welcome-screen'
import { SplashScreen } from '@/components/overlays/splash-screen'
import { isPoemMode } from '@/types/poem'

export default function HomePage() {
  return (
    <Suspense fallback={null}>
      <HomePageContent />
    </Suspense>
  )
}

function HomePageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const poemId = searchParams.get('poemId')
    const viewMode = searchParams.get('viewMode')

    if (!poemId) return

    const params = new URLSearchParams({
      poemId,
    })

    if (isPoemMode(viewMode)) {
      params.set('viewMode', viewMode)
    }

    router.replace(`/dashboard?${params.toString()}`)
  }, [router, searchParams])

  return (
    <>
      <WelcomeScreen />
      <SplashScreen />
    </>
  )
}