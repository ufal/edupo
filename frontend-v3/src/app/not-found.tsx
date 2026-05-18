import Image from 'next/image'
import Link from 'next/link'
import { FullscreenBrandScreen } from '@/components/layout/mobile/fullscreen-brand-screen'
import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <FullscreenBrandScreen>
      <section className="flex grow flex-col items-center justify-evenly text-center">

        <h1 className="typo-h1">ERROR 404</h1>

        <p className="typo-h3">
          Stránka nebyla nalezena
        </p>

        <Image
          src="/assets/girl-puzzled.svg"
          alt=""
          width={260}
          height={260}
          priority
        />
      </section>

      <Button asChild variant="accent" size="sm" className="mx-auto px-6">
        <Link href="/dashboard">
          Vrátit se na hlavní stranu
        </Link>
      </Button>
    </FullscreenBrandScreen>
  )
}