'use client'

import { AppIcon } from "@/components/icons/app-icon"
import Link from 'next/link'

export default function MobilePageNavigationPanel() {
  return (
      <header className="flex h-20 items-center justify-between bg-purple-700 px-5 text-white">
        <div className="flex items-center gap-4">
          <Link href={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "dashboard"} className="mt-3">
            <AppIcon name="arrowLeft" size={24} className="text-white" />
          </Link>
        </div>
      </header>
  )
}