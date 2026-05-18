'use client'

import { useState } from 'react'
import { Check, ChevronDown } from 'lucide-react'
import { cn } from '@/libs/utils'

type PlainSelectOption = {
  value: string
  label: string
}

type PlainSelectProps = {
  value?: string
  placeholder?: string
  emptyLabel?: string
  options: PlainSelectOption[]
  onChange: (value: string) => void
  className?: string
}

export function PlainSelect({
  value,
  placeholder = 'Vyberte možnost',
  emptyLabel = 'Žádné možnosti',
  options,
  onChange,
  className,
}: PlainSelectProps) {
  const [isOpen, setIsOpen] = useState(false)

  const selectedOption = options.find((option) => option.value === value)
  const isEmpty = options.length === 0

  return (
    <>
      {isOpen && !isEmpty && (
        <button
          type="button"
          aria-label="Zavřít výběr"
          onClick={() => setIsOpen(false)}
          className="fixed inset-0 z-80 bg-purple-500/75"
        />
      )}

      <div className={cn('relative', isOpen && 'z-90', className)}>
        <button
          type="button"
          disabled={isEmpty}
          onClick={() => {
            if (isEmpty) return
            setIsOpen((current) => !current)
          }}
          className={cn(
            'flex h-10 w-full items-center justify-between rounded-full bg-white px-4 typo-small text-grey-700',
            isEmpty && 'cursor-not-allowed text-grey-400 opacity-70',
          )}
        >
          <span>
            {isEmpty
              ? emptyLabel
              : selectedOption?.label ?? placeholder}
          </span>

          <ChevronDown
            size={18}
            strokeWidth={2.2}
            className="text-slate-400"
          />
        </button>

        {isOpen && !isEmpty && (
          <div className="absolute left-0 top-11 z-100 w-full rounded-[20px] bg-white px-2 py-2 shadow-lg">
            <div className="max-h-36 overflow-y-auto pr-1">
              {options.map((option) => {
                const isSelected = option.value === value

                return (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => {
                      onChange(option.value)
                      setIsOpen(false)
                    }}
                    className={cn(
                      'flex h-8 w-full items-center rounded-full px-3 text-left typo-small text-grey-700 hover:bg-teal-100',
                      isSelected && 'bg-teal-100 text-grey-900',
                    )}
                  >
                    <span className="mr-3 grid size-4 place-items-center">
                      {isSelected && (
                        <Check
                          size={16}
                          strokeWidth={2.3}
                          className="text-slate-400"
                        />
                      )}
                    </span>

                    <span>{option.label}</span>
                  </button>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </>
  )
}