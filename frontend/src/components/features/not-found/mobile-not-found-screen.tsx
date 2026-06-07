import Image from 'next/image'
import Link from 'next/link'
import { FullscreenBrandScreen } from '@/components/layout/mobile/fullscreen-brand-screen'
import { Button } from '@/components/ui/button'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

export function MobileNotFoundScreen() {
  return (
    <FullscreenBrandScreen>
      <section className="flex grow flex-col items-center justify-evenly text-center">
        <h1 className="typo-h1">ERROR 404</h1>

        <p className="typo-h3">Stránka nebyla nalezena</p>

        <Image
          src={`${base}assets/girl-puzzled.svg`}
          alt=""
          width={260}
          height={260}
          priority
        />
      </section>

      <Button asChild variant="accent" size="sm" className="mx-auto px-6">
        <Link href={`${base}dashboard`}>Vrátit se na hlavní stranu</Link>
      </Button>
    </FullscreenBrandScreen>
  )
}