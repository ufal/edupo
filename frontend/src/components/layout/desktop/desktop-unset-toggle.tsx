'use client'

import { Switch } from '@/components/ui/switch'

type DesktopUnsetToggleProps = {
  label: string
  unset: boolean
  onUnsetChange: (unset: boolean) => void
}

export function DesktopUnsetToggle({
  label,
  unset,
  onUnsetChange,
}: DesktopUnsetToggleProps) {
  return (
    <label className="mt-3 flex w-fit cursor-pointer items-center gap-3">
      <Switch
        aria-label={`${label}: použít vlastní nastavení`}
        checked={!unset}
        onCheckedChange={(checked) => onUnsetChange(!checked)}
      />

      <span className="typo-small text-white">
        {unset ? 'Nenastaveno' : 'Nastavit'}
      </span>
    </label>
  )
}