'use client'

import * as React from 'react'
import { ChevronsUpDown, Plus } from 'lucide-react'

import { Button } from '@/components/ui/button'
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { twMerge } from 'tailwind-merge'

interface ComboboxDataEntry {
  value: string
  label: string
}

interface ComboboxParams {
  withSearch?: boolean
  allowCustomInput?: boolean
  disabled?: boolean
  highlighted?: boolean
  placeholder: string
  data: ComboboxDataEntry[]
  value: string // Selected value OR a free typed string (when allowCustomInput)
  onChange: (value: string) => void
}

export function Combobox({
  withSearch,
  allowCustomInput = false,
  placeholder,
  data,
  disabled,
  highlighted,
  value,
  onChange,
}: ComboboxParams) {
  const [open, setOpen] = React.useState(false)
  const [query, setQuery] = React.useState('')

  // Figure out what to show on the trigger button
  const matched = data.find((d) => d.value === value)
  const displayLabel = matched?.label ?? (allowCustomInput ? value : '')

  const normalized = query.trim().toLowerCase()
  const filtered = normalized
    ? data.filter((d) => d.label.toLowerCase().includes(normalized))
    : data

  const exactLabelExists = normalized
    ? data.some((d) => d.label.toLowerCase() === normalized)
    : false

  // Keep query in sync when opening/closing so typing feels natural
  React.useEffect(() => {
    if (open) {
      // Prefill with current display value for quick editing/searching
      setQuery(displayLabel || '')
    } else {
      setQuery('')
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [open])

  function commitCustom(current: string) {
    const trimmed = current.trim()
    if (!trimmed) return
    onChange(trimmed)
    setOpen(false)
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (!allowCustomInput) return
    if (e.key === 'Enter') {
      // If user presses Enter and nothing highlighted/matching exactly, take the raw text
      const highlighted = (document.querySelector(
        '[cmdk-item][data-selected="true"]'
      ) as HTMLElement | null)?.getAttribute('data-value')
      if (!highlighted) {
        e.preventDefault()
        commitCustom(query)
      }
    }
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          disabled={disabled}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={twMerge('w-full justify-between', highlighted && 'border-blueSoft')}
        >
          {displayLabel || placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[--radix-popover-trigger-width] p-0" align="start">
        <Command shouldFilter={false}>
          {withSearch && (
            <CommandInput
              placeholder={placeholder}
              value={query}
              onValueChange={setQuery}
              onKeyDown={handleKeyDown}
            />
          )}

          <CommandList>
            {/* Empty state */}
            {filtered.length === 0 ? (
              <CommandEmpty>
                <div className="p-2 text-sm">Nic nenalezeno.</div>
                {allowCustomInput && query.trim().length > 0 && !exactLabelExists && (
                  <div className="p-2">
                    <button
                      type="button"
                      className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-left text-sm hover:bg-accent"
                      onClick={() => commitCustom(query)}
                    >
                      <Plus className="h-4 w-4" />
                      Použít „{query.trim()}“
                    </button>
                  </div>
                )}
              </CommandEmpty>
            ) : (
              <>
                {/* Optional creatable row on top */}
                {allowCustomInput && query.trim().length > 0 && !exactLabelExists && (
                  <div className="border-b">
                    <button
                      type="button"
                      className="flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-accent"
                      onClick={() => commitCustom(query)}
                    >
                      <Plus className="h-4 w-4" />
                      Použít „{query.trim()}“
                    </button>
                  </div>
                )}

                <CommandGroup>
                  {filtered.map((d) => (
                    <CommandItem
                      key={d.value}
                      value={d.value}
                      onSelect={() => {
                        onChange(d.value)
                        setOpen(false)
                      }}
                    >
                      {d.label}
                    </CommandItem>
                  ))}
                </CommandGroup>
              </>
            )}
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}