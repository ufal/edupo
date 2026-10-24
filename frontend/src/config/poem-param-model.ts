import type { AvailableModel } from '@/types/edupo-api'

export const LEGACY_DEFAULT_MODEL_SPEC = 'EduPo'

export const LEGACY_MODEL_OPTIONS = [
  { value: 'Komerční rychejší', label: 'Komerční rychejší' },
  { value: 'Komerční lepší', label: 'Komerční lepší' },
  { value: 'EduPo', label: 'EduPo' },
]

const LEGACY_MODEL_IDENTIFIERS: Record<string, string> = {
  'Komerční rychejší': 'fast',
  'Komerční rychlejší': 'fast',
  'Komerční lepší': 'good',
}

export function getDefaultModel(
  models: AvailableModel[],
): AvailableModel | undefined {
  return models.find((model) => model.default)
}

export function findAvailableModel(
  models: AvailableModel[],
  identifier: string | null | undefined,
): AvailableModel | undefined {
  if (!identifier) return undefined

  const normalizedIdentifier =
    LEGACY_MODEL_IDENTIFIERS[identifier] ?? identifier

  return models.find(
    (model) =>
      model.generic_identifier === normalizedIdentifier ||
      model.precise_identifier === normalizedIdentifier,
  )
}