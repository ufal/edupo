export type MetrumOption = 'trochej' | 'jamb' | 'daktyl' | 'volný'

export const DEFAULT_METRUM: MetrumOption = 'trochej'

export const options: { value: MetrumOption; label: string }[] = [
  { value: 'trochej', label: 'Trochej' },
  { value: 'jamb', label: 'Jamb' },
  { value: 'daktyl', label: 'Daktyl' },
  { value: 'volný', label: 'Volný' },
]