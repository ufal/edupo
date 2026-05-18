import type { Poem, PoemLine } from '@/types/poem'
import type { GeneratePoemResponse } from '@/types/edupo-api'

function parsePlaintextToLines(plaintext: string): PoemLine[] {
  return plaintext
    .split('\n')
    .map((line) => line.trim())
    .filter(Boolean)
    .map((text, index) => ({
      id: `line-${index + 1}`,
      text,
    }))
}

export function mapPoemResponseToPoem(
  response: GeneratePoemResponse,
): Poem {
  const text = response.plaintext ?? ''
  const lines = parsePlaintextToLines(text)
  const normalizedText = lines.map((line) => line.text).join('\n')

  return {
    id: response.id,
    title: response.title,
    text: normalizedText,
    originalText: normalizedText,
    lines,
    createdAt: new Date().toISOString(),
  }
}