import { DesktopGenerationOverlay } from './desktop-generation-overlay'
import { MobileGenerationOverlay } from './mobile-generation-overlay'

export function GenerationOverlay() {
  return (
    <>
      <div className="block desktop:hidden">
        <MobileGenerationOverlay />
      </div>

      <div className="hidden desktop:block">
        <DesktopGenerationOverlay />
      </div>
    </>
  )
}