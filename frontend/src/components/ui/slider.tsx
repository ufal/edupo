'use client'

import * as SliderPrimitive from '@radix-ui/react-slider'
import { cn } from '@/libs/utils'

type SliderColorTheme = 'green' | 'yellow'

function Slider({
  colorTheme = 'green',
  className,
  ...props
}: React.ComponentProps<typeof SliderPrimitive.Root> & { colorTheme?: SliderColorTheme }) {
  return (
    <SliderPrimitive.Root
      data-slot="slider"
      className={cn(
        'relative flex w-full touch-none select-none items-center',
        className,
      )}
      {...props}
    >
      <SliderPrimitive.Track className={cn("relative h-1.5 w-full grow overflow-hidden rounded-full", colorTheme === 'green' ? "bg-grey-300" : "bg-white")}>
        <SliderPrimitive.Range className={cn("absolute h-full", colorTheme === 'green' ? "bg-teal-700" : "bg-yellow-400")} />
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