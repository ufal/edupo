import { EdupoLogo } from '@/components/brand/edupo-logo'
import Link from 'next/dist/client/link'

export function DesktopHeader() {
  return (
    <header className="px-[50px] pt-[60px] pb-[29px] flex">
      <Link href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "dashboard"} className="mr-auto inline-flex">
        <EdupoLogo />
      </Link>
    </header>
  )
}