"use client"

import * as React from "react"
import { Check, ChevronsUpDown } from "lucide-react"

import { cn } from "@/lib/utils"
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

interface ComboboxDataEntry {
  value: string;
  label: string;
}

interface ComboboxParams {
  searchInput?: boolean;
  disabled?: boolean;
  highlighted?: boolean;
  placeholder: string;
  data: ComboboxDataEntry[];

  value: string;
  onChange: (value: string) => void;
}

export function Combobox({ searchInput, placeholder, data, disabled, highlighted, value, onChange } : ComboboxParams) {
  const [open, setOpen] = React.useState(false);

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
          {value
            ? data.find((d) => d.value === value)?.label
            : placeholder}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[--radix-popover-trigger-width] p-0">
        <Command>
          {
            (searchInput === true) && <CommandInput placeholder={placeholder} />
          }
          <CommandList>
            <CommandEmpty>Nic nenalezeno.</CommandEmpty>
            <CommandGroup>
              {data.map((d) => (
                <CommandItem
                  key={d.value}
                  value={d.value}
                  onSelect={(currentValue) => {
                    const newValue = currentValue === value ? "" : currentValue;
                    onChange(newValue);
                    setOpen(false);
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
