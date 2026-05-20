import { ReactNode } from 'react'
import { AppIcon, IconName } from '@/components/icons/app-icon'

export function SettingsCard({
  iconName,
  title,
  value,
  onClick,
}: {
  iconName: IconName
  title: string
  value?: ReactNode
  onClick: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className="flex flex-col items-center justify-center gap-2 rounded-[24px] bg-white px-4 py-6 text-center"
    >
      <AppIcon name={iconName} size={42} className="text-purple-500" />

      <div className="text-sm text-zinc-700">
        {title}
      </div>

      {value && (
        <div className="text-xs text-zinc-400">
          {value}
        </div>
      )}
    </button>
  )
}