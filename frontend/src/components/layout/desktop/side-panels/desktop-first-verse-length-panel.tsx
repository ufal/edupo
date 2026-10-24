'use client'

import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopNumberSetting } from './desktop-number-setting'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import {
  FIRST_VERSE_LENGTH_STEP,
  MAX_FIRST_VERSE_LENGTH,
  MIN_FIRST_VERSE_LENGTH,
  isValidFirstVerseLength,
} from '@/config/poem-param-first-verse-length'

type DesktopFirstVerseLengthPanelProps = {
  onClose: () => void
}

export function DesktopFirstVerseLengthPanel({
  onClose,
}: DesktopFirstVerseLengthPanelProps) {
  return (
    <DesktopSidePanelShell
      title={poemParamInfoTexts.firstVerseLength.title}
      infoText={poemParamInfoTexts.firstVerseLength.text}
      onClose={onClose}
    >
      <p className="typo-body font-bold">
        Délka prvního verše (ve slabikách)
      </p>

      <DesktopNumberSetting
        param="firstVerseLength"
        label="Délka verše"
        placeholder="Délka prvního verše"
        min={MIN_FIRST_VERSE_LENGTH}
        max={MAX_FIRST_VERSE_LENGTH}
        step={FIRST_VERSE_LENGTH_STEP}
        isValid={isValidFirstVerseLength}
      />
    </DesktopSidePanelShell>
  )
}