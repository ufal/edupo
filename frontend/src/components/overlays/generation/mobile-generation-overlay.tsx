import { MobileFullscreenOverlay } from '../mobile-fullscreen-overlay'
import { MobileHeader } from '@/components/layout/mobile/mobile-header'
import { GenerationStars } from './generation-stars'

export function MobileGenerationOverlay() {
  return (
    <MobileFullscreenOverlay>
      <div className="flex h-full flex-col">
        <MobileHeader mode="logo-only" />

        <section className="flex grow flex-col items-center justify-center px-8 text-center">
          <div className="-mt-16 mb-16">
            <GenerationStars />
          </div>

          <h2 className="typo-h2 max-w-85 text-white">
            Verše se právě skládají... ještě okamžik.
          </h2>
        </section>
      </div>
    </MobileFullscreenOverlay>
  )
}