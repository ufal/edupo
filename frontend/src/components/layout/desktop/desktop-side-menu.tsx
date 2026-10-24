'use client'

import Link from 'next/link'
import { EdupoLogo } from '@/components/brand/edupo-logo'
import { AppIcon, type IconName } from '@/components/icons/app-icon'
import { Button } from '@/components/ui/button'
import { useGeneratePoemAction } from '@/hooks/use-generate-poem-action'
import { getAuthorStyleById } from '@/services/author-styles-service'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'
import {
  useDesktopSettingsUiStore,
  type DesktopSettingId,
  type DesktopUnsetParam,
} from '@/stores/desktop-settings-ui-store'
import type { PoemGenerationParams } from '@/types/poem'
import type { DesktopSidePanel } from './desktop-side-panel-types'
import authorCollections from '@/data/author-collections.json'
import { usePoemModels } from '@/hooks/use-poem-models'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

type DesktopMenuItem = {
  id: DesktopSettingId
  icon: IconName
  label: string
}

const menuItems: DesktopMenuItem[] = [
  {
    id: 'author-style',
    icon: 'feather',
    label: 'Autorský styl',
  },
  {
    id: 'title-motifs',
    icon: 'book',
    label: 'Název, motiv a nálada',
  },
  {
    id: 'form',
    icon: 'geometry',
    label: 'Pevná forma',
  },
  {
    id: 'verse-count',
    icon: 'verseList',
    label: 'Počet veršů a slok',
  },
  {
    id: 'first-verse-length',
    icon: 'ruler',
    label: 'Délka prvního verše',
  },
  {
    id: 'rhyme-scheme',
    icon: 'verseGroups',
    label: 'Rýmové schéma',
  },
  {
    id: 'metrum',
    icon: 'metrum',
    label: 'Metrum',
  },
  {
    id: 'temperature',
    icon: 'thermometer',
    label: 'AI model',
  },
]

const formLabels = {
  haiku: 'Haiku',
  limerik: 'Limerik',
  sonet: 'Sonet'
} as const

const metrumLabels = {
  daktyl: 'Daktyl',
  jamb: 'Jamb',
  trochej: 'Trochej',
  volný: 'Volný verš'
} as const

function getSettingValue(
  id: DesktopSettingId,
  params: PoemGenerationParams,
  unset: Record<DesktopUnsetParam, boolean>,
  authorLabel?: string,
  collectionId?: string | null,
  modelLabel?: string,
): string {
  switch (id) {
    case 'author-style': {
      const values: string[] = []

      if (!unset.authorStyleId && authorLabel) {
        values.push(authorLabel)
      }

      if (!unset.collectionId && collectionId) {
        const collection = authorCollections.find(
          (item) => item.id === collectionId,
        )

        if (collection) {
          values.push(collection.label)
        }
      }

      return values.join(' · ') || 'Nenastaveno'
    }

    case 'title-motifs': {
      const values = [
        !unset.title ? params.title?.trim() : undefined,

        !unset.motifs
          ? params.motifs
              ?.map((motif) => motif.trim())
              .filter(Boolean)
              .join(', ')
          : undefined,

        !unset.mood ? params.mood : undefined,
      ].filter(Boolean)

      return values.join(' · ') || 'Nenastaveno'
    }

    case 'form':
      return !unset.form && params.form
        ? formLabels[params.form]
        : 'Nenastaveno'

    case 'verse-count': {
      const values: string[] = []

      if (
        !unset.verseCount &&
        typeof params.verseCount === 'number'
      ) {
        values.push(`Verše: ${params.verseCount}`)
      }

      if (
        !unset.maxStrophes &&
        typeof params.maxStrophes === 'number'
      ) {
        values.push(`Max. slok: ${params.maxStrophes}`)
      }

      return values.join(' · ') || 'Nenastaveno'
    }

    case 'first-verse-length':
      return (
        !unset.firstVerseLength &&
        typeof params.firstVerseLength === 'number'
      )
        ? `Slabiky: ${params.firstVerseLength}`
        : 'Nenastaveno'

    case 'rhyme-scheme':
      return !unset.rhymeScheme
        ? params.rhymeScheme || 'Nenastaveno'
        : 'Nenastaveno'

    case 'metrum':
      return !unset.metrum && params.metrum
        ? metrumLabels[params.metrum]
        : 'Nenastaveno'

    case 'temperature': {
      const values: string[] = []

      if (!unset.modelSpec) {
        values.push(modelLabel ?? 'Načítání modelů…')
      }

      if (
        !unset.temperature &&
        typeof params.temperature === 'number'
      ) {
        values.push(`Temperature: ${params.temperature.toFixed(1)}`)
      }

      return values.join(' · ') || 'Nenastaveno'
    }
  }
}

type DesktopSideMenuItemProps = {
  item: DesktopMenuItem
  value: string
  active: boolean
  visible: boolean
  onOpen: () => void
  onToggleVisibility: () => void
}

function DesktopSideMenuItem({
  item,
  value,
  active,
  visible,
  onOpen,
  onToggleVisibility,
}: DesktopSideMenuItemProps) {
  return (
    <div
      className={[
        'flex items-center gap-2 py-[10px]',
        'border-b border-white/30 last:border-b-0',
      ].join(' ')}
    >
      <button
        type="button"
        onClick={onOpen}
        aria-expanded={active}
        className={[
          'flex min-w-0 flex-1 items-center gap-4',
          'rounded-xl text-left cursor-pointer',
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-yellow-300',
        ].join(' ')}
      >
        <span
          className={[
            'grid size-12 shrink-0 place-items-center rounded-2xl',
            active
              ? 'bg-yellow-300 text-grey-900'
              : 'bg-white/20 text-white',
          ].join(' ')}
        >
          <AppIcon name={item.icon} size={23} />
        </span>

        <span className="flex min-w-0 flex-1 flex-col gap-1">
          <span className="typo-body font-medium">
            {item.label}
          </span>

          <span
            title={visible ? value : 'Skryto'}
            className="truncate typo-small"
          >
            {visible ? value : 'Skryto'}
          </span>
        </span>
      </button>

      <button
        type="button"
        onClick={onToggleVisibility}
        aria-label={`${
          visible ? 'Skrýt' : 'Zobrazit'
        } nastavení: ${item.label}`}
        aria-pressed={visible}
        title={visible ? 'Skrýt nastavení' : 'Zobrazit nastavení'}
        className={[
          'grid size-8 shrink-0 place-items-center rounded-lg',
          'cursor-pointer transition-colors', // hover:bg-white/10
          'focus-visible:outline-none focus-visible:ring-2',
          'focus-visible:ring-yellow-300',
        ].join(' ')}
      >
        <AppIcon
          name={visible ? 'eye' : 'eyeOff'}
          size={30}
          className={visible ? 'text-white' : 'text-yellow-300'}
        />
      </button>
    </div>
  )
}

type DesktopSideMenuProps = {
  activePanel: DesktopSidePanel
  onPanelToggle: (panel: Exclude<DesktopSidePanel, null>) => void
}

export function DesktopSideMenu({
  activePanel,
  onPanelToggle,
}: DesktopSideMenuProps) {
  const { runGeneratePoemAction } = useGeneratePoemAction()

  const params = usePoemStore((state) => state.params)
  const selectedAuthorStyleId = usePoemStore(
    (state) => state.selectedAuthorStyleId,
  )
  const status = usePoemStore((state) => state.status)

  const overlay = useUiStore((state) => state.overlay)
  const closeOverlay = useUiStore((state) => state.closeOverlay)

  const visibility = useDesktopSettingsUiStore(
    (state) => state.visibility,
  )
  const toggleVisibility = useDesktopSettingsUiStore(
    (state) => state.toggleVisibility,
  )

  const selectedAuthor = getAuthorStyleById(selectedAuthorStyleId)
  const isGenerating = status === 'loading'

  const unset = useDesktopSettingsUiStore((state) => state.unset)

  const { modelLabel } = usePoemModels()

  function handleOpenSetting(id: DesktopSettingId) {
    closeOverlay()
    onPanelToggle(id)
  }

  function handleResetSettings() {
    usePoemStore.setState({
      params: {},
      selectedAuthorStyleId: null,
    })

    const desktopUi = useDesktopSettingsUiStore.getState()
    desktopUi.resetVisibility()
    desktopUi.resetUnset()
    desktopUi.setSelectedCollectionId(null)

    closeOverlay()

    if (activePanel) {
      onPanelToggle(activePanel)
    }
  }

  const selectedCollectionId = useDesktopSettingsUiStore(
    (state) => state.selectedCollectionId,
  )

  return (
    <aside
      className={[
        'relative z-30 flex min-h-0 flex-col overflow-y-auto',
        'bg-primary px-[50px] py-[60px]',
        'text-primary-foreground',
      ].join(' ')}
    >
      <Link
        href={`${base}dashboard`}
        aria-label="Edupo – hlavní stránka"
        className="inline-flex self-start"
      >
        <EdupoLogo />
      </Link>

      <nav
        aria-label="Nastavení básně"
        className="mt-14 flex flex-col"
      >
        {menuItems.map((item) => (
          <DesktopSideMenuItem
            key={item.id}
            item={item}
            value={getSettingValue(
              item.id,
              params,
              unset,
              selectedAuthor?.label,
              selectedCollectionId,
              modelLabel,
            )}
            active={activePanel === item.id}
            visible={visibility[item.id]}
            onOpen={() => handleOpenSetting(item.id)}
            onToggleVisibility={() => toggleVisibility(item.id)}
          />
        ))}
      </nav>

      <div className="mt-16 flex flex-col gap-4">
        <Button
          type="button"
          variant="subtle"
          size="md"
          disabled={isGenerating}
          onClick={() =>
            void runGeneratePoemAction({ requireParams: true })
          }
          className="w-full shrink-0"
        >
          <AppIcon
            name="stars"
            size={28}
            className="text-subtle-foreground"
          />
          Generovat báseň
        </Button>

        <Button
          type="button"
          variant="ghost"
          size="md"
          disabled={isGenerating}
          onClick={handleResetSettings}
          className={[
            'w-full shrink-0 border border-white',
            'text-white hover:bg-white/10',
          ].join(' ')}
        >
          <AppIcon name="reset" size={28} className="text-white" />
          Resetovat nastavení
        </Button>
      </div>
    </aside>
  )
}