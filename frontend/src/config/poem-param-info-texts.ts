import type { PoemGenerationParams } from '@/types/poem'
import { title } from 'process'

export type PoemParamInfoKey =
  | 'titleMotifs'
  | Extract<
      keyof PoemGenerationParams,
      | 'form'
      | 'verseCount'
      | 'rhymeScheme'
      | 'firstVerseLength'
      | 'metrum'
      | 'temperature'
    >

export type PoemParamInfo = {
  title: string
  text: string
}

export const poemParamInfoTexts: Record<PoemParamInfoKey, PoemParamInfo> = {
  titleMotifs: {
    title: 'Název a motiv',
    text: 'Názvem, volbou až pěti motivů a náladou můžete ovlivnit téma a vyznění generované básně.',
  },

  form: {
    title: 'Pevná forma',
    text: 'Chcete, aby báseň měla nějakou pevnou formu, např. sonet?',
  },

  verseCount: {
    title: 'Počet veršů a slok',
    text: 'Nastavte počet veršů v první sloce a maximální počet slok básně.',
  },

  rhymeScheme: {
    title: 'Rýmové schéma',
    text: 'Pro použití této funkce nastavte počet veršů a nepoužívejte pevnou formu.',
  },

  firstVerseLength: {
    title: 'Délka prvního verše',
    text: 'Kolik slabik má mít první verš?',
  },

  metrum: {
    title: 'Metrum',
    text: 'Obecný princip organizace silných (přízvučných) a slabých (nepřízvučných) pozic verše. Např. trochej, jamb, daktyl.',
  },

  temperature: {
    title: 'AI model',
    text: 'Teplota určuje, jak moc má být AI kreativní. Zároveň můžete vybrat model použitý pro generování.',
  },
}