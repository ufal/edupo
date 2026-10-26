
import type { Poem } from '@/types/poem'
import type { GeneratePoemResponse } from '@/types/edupo-api'
import {
  parsePlaintextToLines,
  serializePoemLines,
} from '@/utils/poem-lines'

export function mapPoemResponseToPoem(
  response: GeneratePoemResponse,
): Poem {
  const lines = parsePlaintextToLines(response.plaintext ?? '')
  const normalizedText = serializePoemLines(lines)

  return {
    id: response.id,
    title: response.title,
    authorName: response.author_name,
    text: normalizedText,
    originalText: normalizedText,
    lines,
    createdAt: new Date().toISOString(),
    source: 'backend',
  }
}
