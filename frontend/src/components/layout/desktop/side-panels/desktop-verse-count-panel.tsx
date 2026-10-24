'use client'

import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopNumberSetting } from './desktop-number-setting'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  MAX_VERSES,
  MIN_VERSES,
  VERSE_COUNT_STEP,
  isValidVerseCount,
} from '@/config/poem-param-verse-count'
import {
  MAX_STROPHES,
  MIN_STROPHES,
  STROPHE_COUNT_STEP,
  isValidMaxStrophes,
} from '@/config/poem-param-max-strophes'

type DesktopVerseCountPanelProps = {
  onClose: () => void
}

export function DesktopVerseCountPanel({
  onClose,
}: DesktopVerseCountPanelProps) {
  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.verseCount.title}
      infoText={poemParamInfoTexts.verseCount.text}
      onClose={onClose}
    >
      <p className="typo-body font-bold">
        Počet veršů ve sloce
      </p>

      <DesktopNumberSetting
        param="verseCount"
        label="Počet veršů"
        placeholder="Počet veršů ve sloce"
        min={MIN_VERSES}
        max={MAX_VERSES}
        step={VERSE_COUNT_STEP}
        isValid={isValidVerseCount}
      />

      <section className="mt-12">
        <p className="typo-body font-bold">
          Maximální počet slok
        </p>

        <DesktopNumberSetting
          param="maxStrophes"
          label="Maximální počet slok"
          placeholder="Maximální počet slok"
          min={MIN_STROPHES}
          max={MAX_STROPHES}
          step={STROPHE_COUNT_STEP}
          isValid={isValidMaxStrophes}
        />
      </section>
    </DesktopSidePanelShell>
  )
}