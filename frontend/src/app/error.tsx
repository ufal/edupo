'use client'

import Image from 'next/image'
import Link from 'next/link'
import { useEffect } from 'react'
import { FullscreenBrandScreen } from '@/components/layout/mobile/fullscreen-brand-screen'
import { Button } from '@/components/ui/button'

type ErrorPageProps = {
  error: Error & { digest?: string }
}

export default function ErrorPage({ error }: ErrorPageProps) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <FullscreenBrandScreen>
      <section className="flex grow flex-col items-center justify-center">
        <h1 className="text-4xl font-bold tracking-wide">
          CHYBA
        </h1>

        <p className="mt-4 text-2xl font-bold">
          Něco se nepovedlo
        </p>

        <Image
          src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/girl-puzzled.svg"}
          alt=""
          width={260}
          height={260}
          priority
          className="mt-14"
        />
      </section>

      <div className="mx-auto flex flex-col gap-3">

        <Button asChild variant="accent" size="sm" className="px-6">
          <Link href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "dashboard"}>
            Zpět se na hlavní stranu
          </Link>
        </Button>
      </div>
    </FullscreenBrandScreen>
  )
}