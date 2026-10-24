'use client'

import * as SliderPrimitive from '@radix-ui/react-slider'
import { cn } from '@/libs/utils'

type SliderColorTheme = 'green' | 'yellow'

type SliderProps =
  React.ComponentProps<typeof SliderPrimitive.Root> & {
    colorTheme?: SliderColorTheme
    empty?: boolean
  }

function Slider({
  colorTheme = 'green',
  empty = false,
  className,
  ...props
}: SliderProps) {
  return (
    <SliderPrimitive.Root
      data-slot="slider"
      className={cn(
        'relative flex w-full touch-none select-none items-center',
        className,
      )}
      {...props}
    >
      <SliderPrimitive.Track
        className={cn(
          'relative h-1.5 w-full grow overflow-hidden rounded-full',
          colorTheme === 'green' ? 'bg-grey-300' : 'bg-white',
        )}
      >
        <SliderPrimitive.Range
          className={cn(
            'absolute h-full',
            colorTheme === 'green'
              ? 'bg-teal-700'
              : 'bg-yellow-400',
            empty && 'invisible',
          )}
        />
      </SliderPrimitive.Track>

      <SliderPrimitive.Thumb className="block size-5 opacity-0" />
    </SliderPrimitive.Root>
  )
}

export { Slider }