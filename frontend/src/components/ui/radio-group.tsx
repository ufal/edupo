'use client'

import * as RadioGroupPrimitive from '@radix-ui/react-radio-group'
import { Circle } from 'lucide-react'
import { cn } from '@/libs/utils'

function RadioGroup({
  className,
  ...props
}: React.ComponentProps<typeof RadioGroupPrimitive.Root>) {
  return (
    <RadioGroupPrimitive.Root
      data-slot="radio-group"
      className={cn('grid gap-2', className)}
      {...props}
    />
  )
}

function RadioGroupItem({
  className,
  ...props
}: React.ComponentProps<typeof RadioGroupPrimitive.Item>) {
  return (
    <RadioGroupPrimitive.Item
      data-slot="radio-group-item"
      className={cn(
        'grid size-[18px] shrink-0 place-items-center',
        'rounded-full border border-purple-200 bg-white',
        'data-[state=checked]:border-yellow-300',
        'data-[state=checked]:bg-transparent',
        'focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-yellow-300 focus-visible:ring-offset-2',
        'disabled:cursor-not-allowed',
        'disabled:border-transparent disabled:bg-purple-200/70',
        'disabled:[&_[data-slot=radio-indicator]]:opacity-40',
        className,
      )}
      {...props}
    >
      <RadioGroupPrimitive.Indicator
        data-slot="radio-indicator"
        className="flex items-center justify-center"
      >
        <Circle className="size-2 fill-yellow-300 text-yellow-300" />
      </RadioGroupPrimitive.Indicator>
    </RadioGroupPrimitive.Item>
  )
}

export { RadioGroup, RadioGroupItem }