import type { ButtonHTMLAttributes } from 'react'
import { cn } from '@/libs/utils'

type IconButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: React.ReactNode
}

export function IconButton({
  children,
  className,
  ...props
}: IconButtonProps) {
  return (
    <button
      type="button"
      className={cn(
        'inline-flex items-center justify-center rounded-full transition-transform active:scale-95',
        className,
      )}
      {...props}
    >
      {children}
    </button>
  )
}