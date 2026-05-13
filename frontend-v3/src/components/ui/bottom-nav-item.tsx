import Link from 'next/link'
import { AppIcon } from '@/components/icons/app-icon'
import { cn } from '@/lib/utils'

type BottomNavItemVariant = 'default' | 'action'

type BottomNavItemProps = {
  icon: 'home' | 'stars' | 'settings'
  label: string
  href?: string
  active?: boolean
  variant?: BottomNavItemVariant
  onClick?: () => void
}

export function BottomNavItem({
  icon,
  label,
  href,
  active = false,
  variant = 'default',
}: BottomNavItemProps) {
  const isAction = variant === 'action'

  return (
    <Link
      href={href!}
      aria-label={label}
      aria-current={active ? 'page' : undefined}
      className={cn(
        'flex flex-col items-center justify-center',
        'transition-transform active:scale-95',
        isAction ? 'gap-0' : 'gap-1',
      )}
    >
      <span
        className={cn(
          'flex items-center justify-center rounded-2xl transition-colors',
          isAction && 'h-14 w-14 bg-teal-700 text-white',
          !isAction && 'h-10 w-10',
          !isAction && active && 'bg-teal-100 text-teal-700',
          !isAction && !active && 'bg-transparent text-grey-500',
        )}
      >
        <AppIcon name={icon} size={isAction ? 40 : 34} />
      </span>

      {!isAction && (
        <span className={cn('typo-detail', active ? 'text-teal-700' : 'text-grey-500')}>
          {label}
        </span>
      )}
    </Link>
  )
}