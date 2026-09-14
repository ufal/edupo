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
    title: 'Forma',
    text: 'Chcete, aby báseň měla nějakou pevnou formu, např. sonet?',
  },

  verseCount: {
    title: 'Počet veršů',
    text: 'Nastavte počet veršů v první sloce a maximální počet slok básně.',
  },

  rhymeScheme: {
    title: 'Rýmové schéma',
    text: 'Rýmové schéma určuje, které verše se mají rýmovat. Stejná písmena označují verše se stejným rýmem, X označuje verš bez rýmu.',
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
    title: 'Temperature',
    text: 'Teplota určuje, jak moc má být AI kreativní. Zároveň můžete vybrat model použitý pro generování.',
  },
}