'use client'

import * as SliderPrimitive from '@radix-ui/react-slider'
import { cn } from '@/libs/utils'

function Slider({
  className,
  ...props
}: React.ComponentProps<typeof SliderPrimitive.Root>) {
  return (
    <SliderPrimitive.Root
      data-slot="slider"
      className={cn(
        'relative flex w-full touch-none select-none items-center',
        className,
      )}
      {...props}
    >
      <SliderPrimitive.Track className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-grey-300">
        <SliderPrimitive.Range className="absolute h-full bg-teal-700" />
      </SliderPrimitive.Track>

      <SliderPrimitive.Thumb
        className="block size-5 opacity-0"
      />
      
      { /*
      <SliderPrimitive.Thumb
        className="block size-5 rounded-full bg-teal-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-700 focus-visible:ring-offset-2"
        aria-label="Temperature"
      />
      */ }
    </SliderPrimitive.Root>
  )
}

export { Slider }