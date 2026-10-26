
import Link from 'next/link'
import { EdupoLogo } from '@/components/brand/edupo-logo'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

type DesktopHeaderProps = {
  variant?: 'navigation' | 'brand'
}

export function DesktopHeader({
  variant = 'navigation',
}: DesktopHeaderProps) {
  if (variant === 'brand') {
    return (
      <header className="px-[50px] pt-[60px] pb-[29px] flex">
        <Link
          href={`${base}dashboard`}
          className="mr-auto inline-flex"
        >
          <EdupoLogo />
        </Link>
      </header>
    )
  }

  return (
    <header className="flex h-[86px] shrink-0 items-center justify-end gap-12 px-10 typo-body text-zinc-900">
      <Link
        href={`${base}about`}
        className="transition-colors hover:text-purple-500"
      >
        O projektu EDUPO
      </Link>

      <Link
        href={`${base}materials`}
        className="transition-colors hover:text-purple-500"
      >
        Materiály pro učitele
      </Link>

      <Link
        href={`${base}contact`}
        className="transition-colors hover:text-purple-500"
      >
        Kontakt
      </Link>
    </header>
  )
}
