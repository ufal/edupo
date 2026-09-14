import type { PoemMood } from '@/types/poem'

export const MOOD_OPTIONS: {
  value: PoemMood
  label: string
}[] = [
  { value: 'veselá', label: 'Veselá' },
  { value: 'smutná', label: 'Smutná' },
]