import Link from 'next/link'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

function DesktopFooterLink({ href, children }: { href: string, children: React.ReactNode }) {
  return (
    <a href={href} className="px-6">
      {children}
    </a>
  )
}

export function DesktopFooter() {
  return (
    <footer className="flex h-20 items-center justify-end gap-4 px-12 typo-body text-zinc-900">
      <DesktopFooterLink href={`${base}about`}>O projektu EDUPO</DesktopFooterLink>
      <DesktopFooterLink href={`${base}materials`}>Materiály pro učitele</DesktopFooterLink>
      <DesktopFooterLink href={`${base}contact`}>Kontakt</DesktopFooterLink>
    </footer>
  )
}