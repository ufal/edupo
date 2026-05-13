'use client'

import { cn } from "@/lib/utils";
import { EdupoLogo } from "../../brand/edupo-logo";
import { Button } from "../../ui/button";
import { MobileMenuButton } from "./mobile-header-button";
import Link from "next/link";
import { useUiStore } from '@/stores/ui-store'

export function MobileHeader({ mode='main' }: { mode?: 'logo-only' | 'main' }) {
  const openOverlay = useUiStore((state) => state.openOverlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  return (
    <header className={cn("bg-primary text-primary-foreground px-5 pt-10 pb-5 flex items-center justify-end gap-2 h-[45px] box-content ", mode === 'main' && 'border-b')}>
      
      <Link href="/dashboard" className="mr-auto" onClick={() => closeOverlay()}>
        <EdupoLogo />
      </Link>
      {
        mode === 'main' && (
          <Button
            variant="accent"
            size="sm"
            onClick={() => openOverlay('poetry-sample')}
          >
            Ukázka poezie
          </Button>
        )
      }
      {
        mode === 'main' && (
          <MobileMenuButton />
        )
      }

    </header>
  )
}