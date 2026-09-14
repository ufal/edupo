import type { PoemModelSpec } from '@/types/poem'

export const DEFAULT_MODEL_SPEC: PoemModelSpec =
  'google/gemini-3.1-pro-preview'

export const MODEL_OPTIONS: {
  value: PoemModelSpec
  label: string
}[] = [
  { value: 'mc', label: 'mc' },
  { value: 'tm', label: 'tm' },
  { value: 'gpt-4o-mini', label: 'gpt-4o-mini' },
  {
    value: 'google/gemini-3.1-pro-preview',
    label: 'google/gemini-3.1-pro-preview',
  },
]

export function getRandomModelSpec(): PoemModelSpec {
  return MODEL_OPTIONS[
    Math.floor(Math.random() * MODEL_OPTIONS.length)
  ].value
}