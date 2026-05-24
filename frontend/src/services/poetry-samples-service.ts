import samples from '@/data/poetry-samples.json'
import type { Poem } from '@/types/poem'

export type PoetrySample = {
  id: string
  label: string
  collectionTitle: string
  author: string
  poem: Poem
}

const poetrySamples = samples as PoetrySample[]

export function getAllPoetrySamples(): PoetrySample[] {
  return poetrySamples
}

export function getPoetrySampleById(id: string): PoetrySample | null {
  return poetrySamples.find((s) => s.id === id) ?? null
}