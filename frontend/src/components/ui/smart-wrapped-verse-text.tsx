'use client'

import { useLayoutEffect, useMemo, useRef, useState } from 'react'
import { useElementWidth } from '@/hooks/use-element-width'

type SplitVerse = {
  firstLine: string
  secondLine: string
}

type SmartWrappedVerseTextProps = {
  text: string
  className?: string
}

function splitByWords(text: string) {
  return text.trim().split(/\s+/).filter(Boolean)
}

export function SmartWrappedVerseText({
  text,
  className,
}: SmartWrappedVerseTextProps) {
  const containerRef = useRef<HTMLDivElement | null>(null)
  const measureRef = useRef<HTMLDivElement | null>(null)
  const width = useElementWidth(containerRef)

  const words = useMemo(() => splitByWords(text), [text])
  const [splitVerse, setSplitVerse] = useState<SplitVerse | null>(null)

  useLayoutEffect(() => {
    const measure = measureRef.current
    if (!measure || !width || words.length <= 1) {
      setSplitVerse(null)
      return
    }

    measure.textContent = text
    const fullHeight = measure.scrollHeight

    measure.textContent = 'Hg'
    const lineHeight = measure.scrollHeight

    if (fullHeight <= lineHeight * 1.25) {
      setSplitVerse(null)
      return
    }

    let bestFirstLine = words[0]
    let bestSecondLine = words.slice(1).join(' ')

    for (let index = 1; index < words.length; index += 1) {
      const candidateFirstLine = words.slice(0, index + 1).join(' ')
      const candidateSecondLine = words.slice(index + 1).join(' ')

      measure.textContent = candidateFirstLine

      if (measure.scrollHeight > lineHeight * 1.25) {
        break
      }

      bestFirstLine = candidateFirstLine
      bestSecondLine = candidateSecondLine
    }

    if (!bestSecondLine) {
      setSplitVerse(null)
      return
    }

    setSplitVerse({
      firstLine: bestFirstLine,
      secondLine: bestSecondLine,
    })
  }, [text, width, words])

  return (
    <div ref={containerRef} className={className}>
      <div
        ref={measureRef}
        aria-hidden="true"
        className="pointer-events-none invisible absolute left-0 top-0 h-auto whitespace-normal"
        style={{
          width,
        }}
      />

      {splitVerse ? (
        <>
          <div>{splitVerse.firstLine}</div>
          <div className="text-right">{splitVerse.secondLine}</div>
        </>
      ) : (
        <div>{text}</div>
      )}
    </div>
  )
}