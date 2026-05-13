'use client'

import { Check, ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

export type RhymeValue = 'A' | 'B' | 'C' | 'X'
export type RhymeDisplayValue = RhymeValue | '-'

const RHYME_VALUES: RhymeValue[] = ['A', 'B', 'C', 'X']

const valueClasses: Record<RhymeDisplayValue, string> = {
  A: 'bg-purple-100 text-zinc-900',
  B: 'bg-cyan-200 text-zinc-900',
  C: 'bg-teal-100 text-zinc-900',
  X: 'bg-yellow-200 text-zinc-900',
  '-': 'bg-zinc-100 text-zinc-900',
}

type RhymeSlotSelectProps = {
  value: RhymeDisplayValue
  disabled?: boolean
  isOpen: boolean
  onOpenChange: (open: boolean) => void
  onChange: (value: RhymeValue) => void
}

export function RhymeSlotSelect({
  value,
  disabled,
  isOpen,
  onOpenChange,
  onChange,
}: RhymeSlotSelectProps) {
  if (disabled || value === '-') {
    return (
      <button
        type="button"
        disabled
        className="flex h-9 min-w-14 items-center justify-center rounded-full bg-grey-300 px-4 typo-small text-zinc-100"
      >
        –
      </button>
    )
  }

  return (
    <>
      {isOpen && (
        <button
          type="button"
          aria-label="Zavřít výběr"
          onClick={() => onOpenChange(false)}
          className="fixed inset-0 z-80 bg-purple-500/75"
        />
      )}

      <div className={cn('relative', isOpen && 'z-90')}>
        <button
          type="button"
          onClick={() => onOpenChange(!isOpen)}
          className={cn(
            'flex h-9 min-w-14 items-center justify-between gap-1 rounded-full px-3.5 typo-small',
            valueClasses[value],
          )}
        >
          {value}
          <ChevronDown size={14} strokeWidth={2.4} className="text-slate-400" />
        </button>

        {isOpen && (
          <div className="absolute left-0 top-11 z-100 w-14.5 rounded-[20px] bg-white p-1 shadow-lg">
            <div className="flex flex-col gap-1">
              {RHYME_VALUES.map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => {
                    onChange(option)
                    onOpenChange(false)
                  }}
                  className={cn(
                    'flex h-9 items-center justify-between rounded-full px-2.5 typo-small',
                    valueClasses[option],
                  )}
                >
                  <span className="w-4 text-left">{option}</span>

                  <span className="grid size-4 place-items-center">
                    {option === value && (
                      <Check size={14} strokeWidth={2.4} className="text-slate-400" />
                    )}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  )
}