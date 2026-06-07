import Image from 'next/image'
import Link from 'next/link'
import { DesktopHeader } from '@/components/layout/desktop/desktop-header'
import { PartnerLogos } from '@/components/brand/partner-logos'
import { Button } from '@/components/ui/button'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

export function DesktopNotFoundScreen() {
  return (
    <div className="fixed inset-0 flex flex-col bg-primary text-primary-foreground">
      <DesktopHeader />

      <main className="flex min-h-0 flex-1 flex-col items-center justify-center text-center">
        <section className="flex flex-col items-center">
          <h1 className="typo-h1 mb-3">ERROR 404</h1>

          <p className="typo-h3 mb-16">Stránka nebyla nalezena</p>

          <Image
            src={`${base}assets/girl-puzzled.svg`}
            alt=""
            width={320}
            height={320}
            priority
            className="mb-20"
          />

          <Button asChild variant="accent" size="sm" className="px-6">
            <Link href={`${base}dashboard`}>
              Vrátit se na hlavní stranu
            </Link>
          </Button>
        </section>
      </main>

      <footer className="px-[50px] pb-[38px]">
        <PartnerLogos variant="horizontal" set="reduced" />
      </footer>
    </div>
  )
}