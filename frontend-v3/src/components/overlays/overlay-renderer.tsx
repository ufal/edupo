'use client'

import { useUiStore } from '@/stores/ui-store'
import { MissingParamsOverlay } from './missing-params-overlay'
import { MobileMenuOverlay } from './mobile-menu-overlay'
import { GenerationOverlay } from './generation/generation-overlay'
import { PoetrySampleOverlay } from './poetry-sample-overlay'
import { AuthorStyleOverlay } from './author-style-overlay'
import { SettingTitleMotifsOverlay } from './param-settings/setting-title-motifs-overlay'
import { SettingFormOverlay } from './param-settings/setting-form-overlay'
import { SettingVerseCountOverlay } from './param-settings/setting-verse-count-overlay'
import { SettingRhymeSchemeOverlay } from './param-settings/setting-rhyme-scheme-overlay'
import { SettingMetrumOverlay } from './param-settings/setting-metrum-overlay'
import { SettingTemperatureOverlay } from './param-settings/setting-temperature-overlay'
import { SettingFirstVerseLengthOverlay } from './param-settings/setting-first-verse-length-overlay'
import { ShareOverlay } from './share-overlay'

export function OverlayRenderer() {
  const overlay = useUiStore((state) => state.overlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  if (overlay === 'missing-params') {
    return <MissingParamsOverlay onClose={closeOverlay} />
  }

  if (overlay === 'mobile-menu') {
    return <MobileMenuOverlay onClose={closeOverlay} />
  }

  if (overlay === 'generation') {
    return <GenerationOverlay />
  }

  if (overlay === 'poetry-sample') {
    return <PoetrySampleOverlay onClose={closeOverlay} />
  }

  if (overlay === 'author-style') {
    return <AuthorStyleOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-title-motifs') {
    return <SettingTitleMotifsOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-form') {
    return <SettingFormOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-verse-count') {
    return <SettingVerseCountOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-rhyme-scheme') {
    return <SettingRhymeSchemeOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-first-verse-length') {
    return <SettingFirstVerseLengthOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-metrum') {
    return <SettingMetrumOverlay onClose={closeOverlay} />
  }

  if (overlay === 'setting-param-temperature') {
    return <SettingTemperatureOverlay onClose={closeOverlay} />
  }

  if (overlay === 'share') {
    return <ShareOverlay onClose={closeOverlay} />
  }

  return null
}