export type MetrumOption = 'trochej' | 'jamb' | 'daktyl' | 'volný'

export const DEFAULT_METRUM: MetrumOption = 'trochej'

export const options: { value: MetrumOption; label: string }[] = [
  { value: 'daktyl', label: 'Daktyl' },
  { value: 'jamb', label: 'Jamb' },
  { value: 'trochej', label: 'Trochej' },
  { value: 'volný', label: 'Volný' }
]