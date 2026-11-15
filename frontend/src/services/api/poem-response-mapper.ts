
import type { Poem } from '@/types/poem'
import type { GeneratePoemResponse } from '@/types/edupo-api'
import {
  parsePlaintextToLines,
  serializePoemLines,
} from '@/utils/poem-lines'

export function mapPoemResponseToPoem(
  response: GeneratePoemResponse,
  knownOrigin?: Poem['origin'],
): Poem {
  const lines = parsePlaintextToLines(response.plaintext ?? '')
  const normalizedText = serializePoemLines(lines)

  const authorName = response.author_name ?? ''

  const origin =
    knownOrigin ??
    (/\[vygenerováno\]\s*$/i.test(authorName)
      ? 'generated'
      : /\[vloženo uživatelem\]\s*$/i.test(authorName)
        ? 'user'
        : 'unknown')

  return {
    id: response.id,
    title: response.title,
    authorName: response.author_name,
    text: normalizedText,
    originalText: normalizedText,
    lines,
    createdAt: new Date().toISOString(),
    source: 'backend',
    origin,
  }
}
