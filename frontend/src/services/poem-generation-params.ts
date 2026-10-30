
import type { PoemGenerationParams } from '@/types/poem'
import type { GeneratePoemParams } from '@/types/edupo-api'
import authorCollections from '@/data/author-collections.json'

export type GenerationUnsetState = Partial<
  Record<keyof PoemGenerationParams | 'collectionId', boolean>
>

export function buildGenerationParams(
  params: PoemGenerationParams,
  unset?: GenerationUnsetState,
  collectionId?: string | null,
): GeneratePoemParams {
  const enabled = (key: keyof GenerationUnsetState) =>
    unset?.[key] !== true

  const activeForm = enabled('form')
    ? params.form
    : undefined

  const activeAuthorId = enabled('authorStyleId')
    ? params.authorStyleId
    : undefined

  const activeCollection =
    enabled('collectionId') && collectionId
      ? authorCollections.find(
          (item) => item.id === collectionId,
        )
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

    authorStyleId: activeAuthorId,

    collectionId: activeCollection?.id,
  }
}
