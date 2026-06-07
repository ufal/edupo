import { PartnerLogos } from '@/components/brand/partner-logos'
import { DesktopHeader } from '@/components/layout/desktop/desktop-header'
import { GenerationStars } from './generation-stars'

export function DesktopGenerationOverlay() {
  return (
    <div className="fixed inset-0 z-50 flex flex-col bg-primary text-primary-foreground">
      <DesktopHeader />

      <main className="flex min-h-0 flex-1 flex-col items-center justify-center text-center">
        <section className="flex -translate-y-6 flex-col items-center">
          <div className="mb-12">
            <GenerationStars />
          </div>

          <h2 className="typo-h2 font-bold max-w-[430px]">
            Verše se právě skládají...<br />ještě okamžik.
          </h2>
        </section>
      </main>

      <footer className="pb-[65px]">
        <PartnerLogos variant="horizontal" className="justify-center" />
      </footer>
    </div>
  )
}