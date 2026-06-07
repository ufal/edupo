import { DesktopNotFoundScreen } from '@/components/features/not-found/desktop-not-found-screen'
import { MobileNotFoundScreen } from '@/components/features/not-found/mobile-not-found-screen'

export default function NotFound() {
  return (
    <>
      <div className="block desktop:hidden">
        <MobileNotFoundScreen />
      </div>

      <div className="hidden desktop:block">
        <DesktopNotFoundScreen />
      </div>
    </>
  )
}