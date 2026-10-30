
import type { PoemLine } from '@/types/poem'

export function parsePlaintextToLines(
  plaintext: string,
): PoemLine[] {
  const normalized = plaintext.replace(/\r\n?/g, '\n').trim()

  if (!normalized) return []

  const stanzas = normalized
    .split(/\n\s*\n/)
    .map((stanza) =>
      stanza
        .split('\n')
        .map((line) => line.trim())
        .filter(Boolean),
    )
    .filter((stanza) => stanza.length > 0)

  let lineIndex = 0

  return stanzas.flatMap((stanza, stanzaIndex) =>
    stanza.map((text, indexInStanza) => {
      lineIndex += 1

      return {
        id: `line-${lineIndex}`,
        text,
        originalText: text,
        stanzaStart:
          stanzaIndex > 0 && indexInStanza === 0,
      }
    }),
  )
}

export function serializePoemLines(
  lines: PoemLine[],
): string {
  return lines
    .map((line, index) => {
      const separator =
        index === 0
          ? ''
          : line.stanzaStart
            ? '\n\n'
            : '\n'

      return separator + line.text
    })
    .join('')
}


export function getOriginalLineText(
  originalText: string | undefined,
  lineId: string,
): string | undefined {
  if (!originalText) return undefined

  return parsePlaintextToLines(originalText)
    .find((line) => line.id === lineId)
    ?.text
}


export function movePoemLine(
  lines: PoemLine[],
  sourceId: string,
  targetId: string,
): PoemLine[] {
  const sourceIndex = lines.findIndex(
    (line) => line.id === sourceId,
  )

  const targetIndex = lines.findIndex(
    (line) => line.id === targetId,
  )

  if (
    sourceIndex === -1 ||
    targetIndex === -1 ||
    sourceIndex === targetIndex
  ) {
    return lines
  }

  const stanzaPositions = new Set(
    lines.flatMap((line, index) =>
      line.stanzaStart ? [index] : [],
    ),
  )

  const result = [...lines]
  const [movedLine] = result.splice(sourceIndex, 1)
  result.splice(targetIndex, 0, movedLine)

  return result.map((line, index) => ({
    ...line,
    stanzaStart:
      index > 0 && stanzaPositions.has(index),

    group: undefined,
  }))
}
