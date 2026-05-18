'use client'

import { IconButton } from '@/components/ui/icon-button'
import { AppIcon } from '@/components/icons/app-icon'
import { useUiStore } from '@/stores/ui-store'

export function MobileMenuButton() {
  const overlay = useUiStore((state) => state.overlay)
  const openOverlay = useUiStore((state) => state.openOverlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  const isOpen = overlay === 'mobile-menu'

  function handleClick() {
    if (isOpen) {
      closeOverlay()
    } else {
      openOverlay('mobile-menu')
    }
  }

  return (
    <IconButton
      aria-label="Otevřít menu"
      onClick={handleClick}
      className="text-white"
    >
      <AppIcon name="hamburger" size={42} />
    </IconButton>
  )
}