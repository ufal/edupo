import { ComponentProps } from 'react'
import { cn } from '@/libs/utils'

export function Input({
  className,
  ...props
}: ComponentProps<'input'>) {
  return (
    <input
      className={cn(
        'h-11 w-full rounded-full bg-white px-4 typo-body text-grey-900 outline-none',
        'placeholder:text-grey-400',
        'focus:ring-2 focus:ring-zinc-400',
        className,
      )}
      {...props}
    />
  )
}