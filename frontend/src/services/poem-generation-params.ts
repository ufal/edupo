import type { PoemGenerationParams } from '@/types/poem'
import type { GeneratePoemParams } from '@/types/edupo-api'

export type GenerationUnsetState = Partial<
  Record<keyof PoemGenerationParams, boolean>
>

export function buildGenerationParams(
  params: PoemGenerationParams,
  unset?: GenerationUnsetState,
): GeneratePoemParams {
  const enabled = (key: keyof PoemGenerationParams) =>
    unset?.[key] !== true

  const activeForm = enabled('form')
    ? params.form
    : undefined

  return {
    title: enabled('title')
      ? params.title || undefined
      : undefined,

    motifs:
      enabled('motifs') && params.motifs?.length
        ? [...params.motifs]
        : undefined,

    mood: enabled('mood')
      ? params.mood
      : undefined,

    form: activeForm,

    verseCount: enabled('verseCount')
      ? params.verseCount
      : undefined,

    maxStrophes: enabled('maxStrophes')
      ? params.maxStrophes
      : undefined,

    rhymeScheme:
      enabled('rhymeScheme') && !activeForm
        ? params.rhymeScheme || undefined
        : undefined,

    firstVerseLength: enabled('firstVerseLength')
      ? params.firstVerseLength
      : undefined,

    metrum: enabled('metrum')
      ? params.metrum
      : undefined,

    temperature: enabled('temperature')
      ? params.temperature
      : undefined,

    modelSpec: enabled('modelSpec')
      ? params.modelSpec
      : undefined,

    authorStyleId: enabled('authorStyleId')
      ? params.authorStyleId
      : undefined,
  }
}