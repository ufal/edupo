'use client'

import { useEffect } from 'react'
import { useModelsStore } from '@/stores/models-store'
import { usePoemStore } from '@/stores/poem-store'
import {
  findAvailableModel,
  getDefaultModel,
} from '@/config/poem-param-model'

export function usePoemModels() {
  const models = useModelsStore((state) => state.models)
  const status = useModelsStore((state) => state.status)
  const error = useModelsStore((state) => state.error)
  const loadModels = useModelsStore((state) => state.loadModels)

  const storedModelSpec = usePoemStore(
    (state) => state.params.modelSpec,
  )

  useEffect(() => {
    if (status !== 'idle') return

    void loadModels().catch(() => {
      // Chybu zpřístupňuje store přes status a error.
    })
  }, [status, loadModels])

  const selectedModel =
    findAvailableModel(models, storedModelSpec) ??
    getDefaultModel(models)

  const modelOptions = models.map((model) => ({
    value: model.generic_identifier,
    label: model.human_readable_identifier,
  }))

  function retryModels() {
    void loadModels().catch(() => {
      // Chybu zpřístupňuje store.
    })
  }

  return {
    models,
    status,
    error,
    selectedModel,
    modelSpec: selectedModel?.generic_identifier ?? '',
    modelLabel:
      selectedModel?.human_readable_identifier ??
      (status === 'error'
        ? 'Modely se nepodařilo načíst'
        : 'Načítání modelů…'),
    modelOptions,
    retryModels,
  }
}