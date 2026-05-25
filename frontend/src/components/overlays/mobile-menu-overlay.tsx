import Link from 'next/link'
import { ShellOverlay } from './shell-overlay'
import { X } from 'lucide-react'

type MobileMenuOverlayProps = {
  onClose: () => void
}

export function MobileMenuOverlay({ onClose }: MobileMenuOverlayProps) {
  return (
    <ShellOverlay variant="menu">
      <X className="absolute right-7 top-7 cursor-pointer text-white" onClick={onClose} />
      <nav className="flex h-full flex-col items-center pt-24 text-center text-white">
        <Link
          href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "about"}
          onClick={onClose}
          className="typo-h4 mb-12"
        >
          O projektu
        </Link>

        <Link
          href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "materials"}
          onClick={onClose}
          className="typo-h4 mb-12"
        >
          Materiály pro učitele
        </Link>

        <Link
          href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "methodology"}
          onClick={onClose}
          className="typo-h4 mb-12"
        >
          Metodika výuky
        </Link>

        <Link
          href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "contact"}
          onClick={onClose}
          className="typo-h4"
        >
          Kontakt
        </Link>
      </nav>
    </ShellOverlay>
  )
}