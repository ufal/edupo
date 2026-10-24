import { create } from 'zustand'
import { fetchModelsApi } from '@/services/api/models-api'
import type { AvailableModel } from '@/types/edupo-api'

type ModelsStatus = 'idle' | 'loading' | 'success' | 'error'

type ModelsState = {
  models: AvailableModel[]
  status: ModelsStatus
  error: string | null
  loadModels: () => Promise<AvailableModel[]>
}

let pendingRequest: Promise<AvailableModel[]> | null = null

export const useModelsStore = create<ModelsState>((set, get) => ({
  models: [],
  status: 'idle',
  error: null,

  loadModels: () => {
    if (pendingRequest) return pendingRequest

    if (get().status === 'success') {
      return Promise.resolve(get().models)
    }

    set({ status: 'loading', error: null })

    pendingRequest = fetchModelsApi()
      .then((models) => {
        set({
          models,
          status: 'success',
          error: null,
        })

        return models
      })
      .catch((error: unknown) => {
        set({
          status: 'error',
          error:
            error instanceof Error
              ? error.message
              : 'Nepodařilo se načíst AI modely.',
        })

        throw error
      })
      .finally(() => {
        pendingRequest = null
      })

    return pendingRequest
  },
}))