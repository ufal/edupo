'use client'

import {
  useEffect,
  useRef,
  useState,
} from 'react'
import { ChevronDown, Search } from 'lucide-react'
import { cn } from '@/libs/utils'

export type SearchableSelectOption = {
  value: string
  label: string
  group?: string
}

type SearchableSelectProps = {
  label: string
  value?: string | null
  options: SearchableSelectOption[]
  placeholder: string
  searchPlaceholder: string
  disabled?: boolean
  onChange: (value: string) => void
  className?: string
}

function normalizeSearch(value: string) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim()
}

export function SearchableSelect({
  label,
  value,
  options,
  placeholder,
  searchPlaceholder,
  disabled = false,
  onChange,
  className,
}: SearchableSelectProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [query, setQuery] = useState('')

  const rootRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const selectedOption = options.find(
    (option) => option.value === value,
  )

  const normalizedQuery = normalizeSearch(query)

  const filteredOptions = options.filter((option) =>
    normalizeSearch(
      `${option.label} ${option.group ?? ''}`,
    ).includes(normalizedQuery),
  )

  const groups = new Map<string, SearchableSelectOption[]>()

  for (const option of filteredOptions) {
    const group = option.group ?? ''
    const currentOptions = groups.get(group) ?? []

    currentOptions.push(option)
    groups.set(group, currentOptions)
  }

  useEffect(() => {
    if (!isOpen) return
    inputRef.current?.focus()
  }, [isOpen])

  useEffect(() => {
    if (!disabled) return

    setIsOpen(false)
    setQuery('')
  }, [disabled])

  useEffect(() => {
    if (!isOpen) return

    function handleOutsideClick(event: PointerEvent) {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setIsOpen(false)
        setQuery('')
      }
    }

    document.addEventListener('pointerdown', handleOutsideClick)

    return () => {
      document.removeEventListener(
        'pointerdown',
        handleOutsideClick,
      )
    }
  }, [isOpen])

  function closeAndFocusTrigger() {
    setIsOpen(false)
    setQuery('')

    requestAnimationFrame(() => {
      triggerRef.current?.focus()
    })
  }

  return (
    <div
      ref={rootRef}
      className={className}
      onBlur={(event) => {
        if (
          !event.relatedTarget ||
          !event.currentTarget.contains(event.relatedTarget)
        ) {
          setIsOpen(false)
          setQuery('')
        }
      }}
      onKeyDown={(event) => {
        if (event.key === 'Escape' && isOpen) {
          event.preventDefault()
          event.stopPropagation()
          closeAndFocusTrigger()
        }
      }}
    >
      <button
        ref={triggerRef}
        type="button"
        disabled={disabled}
        aria-label={label}
        aria-expanded={isOpen}
        onClick={() => {
          setQuery('')
          setIsOpen((open) => !open)
        }}
        className={cn(
          'flex h-11 w-full items-center justify-between gap-3',
          'rounded-full bg-white px-4 typo-body text-grey-700',
          'cursor-pointer',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-yellow-300',
          'disabled:cursor-not-allowed',
          'disabled:bg-purple-200/70',
          isOpen && 'hidden',
        )}
      >
        <span className="min-w-0 truncate">
          {selectedOption?.label ?? placeholder}
        </span>

        <ChevronDown
          size={18}
          className="shrink-0 text-grey-500"
        />
      </button>

      {isOpen && !disabled && (
        <div
          role="group"
          aria-label={label}
          className="rounded-3xl bg-white p-3 text-grey-700"
        >
          <div className="flex items-center gap-2 border-b border-grey-100 px-2 pb-3">
            <Search
              size={18}
              className="shrink-0 text-grey-400"
            />

            <input
              ref={inputRef}
              type="search"
              aria-label={searchPlaceholder}
              placeholder={searchPlaceholder}
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              className={[
                'h-8 min-w-0 flex-1 bg-transparent',
                'typo-small text-grey-700 outline-none',
                'placeholder:text-grey-400',
              ].join(' ')}
            />
          </div>

          <div className="mt-2 max-h-72 overflow-y-auto">
            {Array.from(groups.entries()).map(
              ([group, groupOptions]) => (
                <div key={group} className="mb-2 last:mb-0">
                  {group && (
                    <p className="px-3 py-2 typo-small text-grey-400">
                      {group}
                    </p>
                  )}

                  {groupOptions.map((option) => (
                    <button
                      key={option.value}
                      type="button"
                      aria-pressed={option.value === value}
                      onClick={() => {
                        onChange(option.value)
                        closeAndFocusTrigger()
                      }}
                      className={cn(
                        'block w-full rounded-lg px-3 py-2',
                        'text-left typo-body text-grey-700',
                        'cursor-pointer hover:bg-teal-100',
                        'focus-visible:outline-none',
                        'focus-visible:bg-teal-100',
                        option.value === value && 'bg-teal-100',
                      )}
                    >
                      {option.label}
                    </button>
                  ))}
                </div>
              ),
            )}

            {filteredOptions.length === 0 && (
              <p className="px-3 py-4 typo-small text-grey-500">
                Nic jsme nenašli.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  )
}