"use client"

import * as React from "react"
import { ChevronsUpDown } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { twMerge } from "tailwind-merge"
import { Input } from "@/components/ui/input"

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
  value: string
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
  const [inputValue, setInputValue] = React.useState("")

  React.useEffect(() => {
    const matched = data.find((d) => d.value === value)
    if (matched) setInputValue(matched.label)
    else if (allowCustomInput) setInputValue(value)
  }, [value, data, allowCustomInput])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault()
      onChange(inputValue)
      setOpen(false)
    }
  }

  const displayLabel =
    data.find((d) => d.value === value)?.label ?? (allowCustomInput ? value : "")

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          disabled={disabled}
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={twMerge("w-full justify-between", highlighted && "border-blueSoft")}
        >
          {displayLabel || placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[--radix-popover-trigger-width] p-0">
        <Command>
          {withSearch && allowCustomInput && (
            <div className="p-2">
              <Input
                placeholder={placeholder}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
              />
            </div>
          )}

          {withSearch && !allowCustomInput && (
            <CommandInput placeholder={placeholder} />
          )}

          <CommandList>
            <CommandEmpty>Nic nenalezeno.</CommandEmpty>
            <CommandGroup>
              {data.map((d) => (
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
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}