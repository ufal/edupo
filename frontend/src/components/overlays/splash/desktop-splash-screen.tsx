import { PartnerLogos } from '@/components/brand/partner-logos'
import { DesktopHeader } from '@/components/layout/desktop/desktop-header'

type DesktopSplashScreenProps = {
  isFading: boolean
}

export function DesktopSplashScreen({ isFading }: DesktopSplashScreenProps) {
  return (
    <div className="fixed inset-0 z-[100] bg-primary text-primary-foreground">
      <div
        className={[
          'flex h-full flex-col',
          'transition-opacity duration-300',
          isFading ? 'opacity-0' : 'opacity-100',
        ].join(' ')}
      >
        <DesktopHeader />

        <main className="flex flex-1 items-center justify-center">
          <div className="mt-[-30px]">
            <PartnerLogos variant="horizontal" />
          </div>
        </main>
      </div>
    </div>
  )
}