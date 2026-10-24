'use client'

import * as SwitchPrimitive from '@radix-ui/react-switch'
import { cn } from '@/libs/utils'

export function Switch({
  className,
  ...props
}: React.ComponentProps<typeof SwitchPrimitive.Root>) {
  return (
    <SwitchPrimitive.Root
      data-slot="switch"
      className={cn(
        'relative inline-flex h-6 w-11 shrink-0 items-center',
        'rounded-full cursor-pointer transition-colors',
        'data-[state=unchecked]:bg-purple-200/70',
        'data-[state=checked]:bg-white',
        'focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-yellow-300 focus-visible:ring-offset-2',
        'focus-visible:ring-offset-purple-600',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className,
      )}
      {...props}
    >
      <SwitchPrimitive.Thumb
        data-slot="switch-thumb"
        className={cn(
          'pointer-events-none absolute left-[2px]',
          'size-5 rounded-full transition-[transform,background-color]',
          'data-[state=unchecked]:translate-x-0',
          'data-[state=unchecked]:bg-white',
          'data-[state=checked]:translate-x-5',
          'data-[state=checked]:bg-purple-600',
        )}
      />
    </SwitchPrimitive.Root>
  )
}