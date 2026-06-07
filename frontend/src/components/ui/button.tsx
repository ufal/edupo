import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cn } from '@/libs/utils'

type ButtonVariant =
  | 'primary'
  | 'accent'
  | 'secondary'
  | 'destructive'
  | 'cancel'
  | 'subtle'
  | 'ghost'
  | 'link'

type ButtonSize =
  | 'sm'
  | 'md'
  | 'lg'
  | 'icon'

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant
  size?: ButtonSize
  leftIcon?: ReactNode
  rightIcon?: ReactNode
  isLoading?: boolean
  asChild?: boolean
}

const variantClasses: Record<ButtonVariant, string> = {
  primary:
    'bg-teal-700 text-white hover:bg-teal-800',

  accent:
    'bg-yellow-300 text-grey-900 hover:bg-yellow-400',

  secondary:
    'bg-purple-500 text-white hover:bg-purple-600',

  destructive:
    'bg-destructive text-destructive-foreground hover:bg-destructive-hover',

  cancel:
    'bg-white text-foreground border border-primary hover:bg-teal-50',

  subtle:
    'bg-subtle text-subtle-foreground hover:bg-subtle-hover',

  ghost:
    'bg-transparent text-foreground hover:bg-grey-50',

  link:
    'bg-transparent text-purple-500 underline underline-offset-4 hover:text-purple-600 p-0 h-auto rounded-none',
}

const sizeClasses: Record<ButtonSize, string> = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-10 px-5 text-sm',
  lg: 'h-12 px-6 text-base',
  icon: 'h-10 w-10 p-0',
}

export function Button({
  children,
  variant = 'primary',
  size = 'md',
  leftIcon,
  rightIcon,
  isLoading = false,
  disabled,
  className,
  asChild = false,
  ...props
}: ButtonProps) {
  const isDisabled = disabled || isLoading

  const classes = cn(
    'inline-flex items-center justify-center gap-2 rounded-full transition-colors cursor-pointer',
    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2',
    'disabled:pointer-events-none disabled:opacity-60',
    variantClasses[variant],
    sizeClasses[size],
    className,
  )

  if (asChild) {
    return (
      <Slot className={classes} {...props}>
        {children}
      </Slot>
    )
  }

  return (
    <button
      className={classes}
      disabled={isDisabled}
      {...props}
    >
      {isLoading ? (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
      ) : (
        leftIcon
      )}

      {size !== 'icon' && children}

      {!isLoading && rightIcon}
    </button>
  )
}