import { PoemForm } from '@/types/poem'

export const DEFAULT_FORM: PoemForm = 'free'

export const options: { value: PoemForm; label: string }[] = [
  { value: 'free', label: 'Volná forma' },
  { value: 'sonet', label: 'Sonet' },
  { value: 'limerik', label: 'Limerik' },
  { value: 'haiku', label: 'Haiku' },
  { value: 'epigram', label: 'Epigram' },
]