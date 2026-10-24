import { apiGetJson } from './http-client'
import type { AvailableModel } from '@/types/edupo-api'

function isAvailableModel(value: unknown): value is AvailableModel {
  if (!value || typeof value !== 'object') return false

  const model = value as Record<string, unknown>

  return (
    typeof model.generic_identifier === 'string' &&
    model.generic_identifier.trim().length > 0 &&
    typeof model.human_readable_identifier === 'string' &&
    model.human_readable_identifier.trim().length > 0 &&
    typeof model.precise_identifier === 'string' &&
    model.precise_identifier.trim().length > 0 &&
    typeof model.default === 'boolean' &&
    typeof model.fallback === 'boolean'
  )
}

export async function fetchModelsApi(): Promise<AvailableModel[]> {
  const response = await apiGetJson<unknown>('get_models')

  if (
    !response ||
    typeof response !== 'object' ||
    !('models' in response) ||
    !Array.isArray(response.models) ||
    response.models.length === 0 ||
    !response.models.every(isAvailableModel)
  ) {
    throw new Error('Backend vrátil neplatný seznam AI modelů.')
  }

  const models = response.models

  const identifiers = new Set(
    models.map((model) => model.generic_identifier),
  )

  if (identifiers.size !== models.length) {
    throw new Error('Backend vrátil duplicitní identifikátory AI modelů.')
  }

  if (models.filter((model) => model.default).length !== 1) {
    throw new Error('Backend musí určit právě jeden výchozí AI model.')
  }

  return models
}