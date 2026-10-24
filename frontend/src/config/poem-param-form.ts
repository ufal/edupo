import { PoemForm } from '@/types/poem'

export const DEFAULT_FORM: PoemForm = 'haiku'

export const options: { value: PoemForm; label: string }[] = [
  { value: 'haiku', label: 'Haiku' },
  { value: 'limerik', label: 'Limerik' },
  { value: 'sonet', label: 'Sonet' }
]