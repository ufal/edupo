import { PartnerLogos } from '@/components/brand/partner-logos'
import { MobileHeader } from '@/components/layout/mobile/mobile-header'
import { MobileFullscreenOverlay } from '../mobile-fullscreen-overlay'

type MobileSplashScreenProps = {
  isFading: boolean
}

export function MobileSplashScreen({ isFading }: MobileSplashScreenProps) {
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

        <section className="flex grow items-stretch justify-center px-8 pt-10 pb-24">
          <PartnerLogos variant="vertical" />
        </section>
      </div>
    </MobileFullscreenOverlay>
  )
}