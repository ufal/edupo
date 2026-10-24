'use client'

import { useId, useState } from 'react'
import { Plus } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { MAX_MOTIFS } from '@/config/poem-param-title-motifs'
import { MOOD_OPTIONS } from '@/config/poem-param-mood'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopUnsetToggle } from './../desktop-unset-toggle'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { AppIcon } from '@/components/icons/app-icon'
import type { PoemMood } from '@/types/poem'

const EMPTY_MOTIFS: string[] = []

const inputClassName = [
  'disabled:cursor-not-allowed',
  'disabled:bg-purple-200/70',
  'focus:ring-yellow-300',
].join(' ')

type DesktopTitleMotifsPanelProps = {
  onClose: () => void
}

export function DesktopTitleMotifsPanel({
  onClose,
}: DesktopTitleMotifsPanelProps) {
  const inputId = useId()

  const title = usePoemStore((state) => state.params.title ?? '')
  const motifs = usePoemStore(
    (state) => state.params.motifs ?? EMPTY_MOTIFS,
  )
  const mood = usePoemStore((state) => state.params.mood)
  const updateParams = usePoemStore((state) => state.updateParams)

  const titleUnset = useDesktopSettingsUiStore(
    (state) => state.unset.title,
  )
  const motifsUnset = useDesktopSettingsUiStore(
    (state) => state.unset.motifs,
  )
  const moodUnset = useDesktopSettingsUiStore(
    (state) => state.unset.mood,
  )
  const setUnset = useDesktopSettingsUiStore(
    (state) => state.setUnset,
  )

  const [motifInputs, setMotifInputs] = useState<string[]>(
    () => (motifs.length ? [...motifs] : ['']),
  )

  function updateMotif(index: number, value: string) {
    const nextInputs = [...motifInputs]
    nextInputs[index] = value

    setMotifInputs(nextInputs)

    updateParams({
      motifs: nextInputs.map((motif) => motif.trim()).filter(Boolean),
    })
  }

  function addMotif() {
    if (motifsUnset) return

    setMotifInputs((current) =>
      current.length < MAX_MOTIFS ? [...current, ''] : current,
    )
  }

  function removeMotif(index: number) {
    if (motifsUnset) return

    const remainingInputs = motifInputs.filter(
      (_, currentIndex) => currentIndex !== index,
    )

    // Po odstranění posledního motivu ponecháme jedno prázdné pole.
    const nextInputs = remainingInputs.length > 0
      ? remainingInputs
      : ['']

    setMotifInputs(nextInputs)

    updateParams({
      motifs: nextInputs
        .map((motif) => motif.trim())
        .filter(Boolean),
    })
  }

  return (
    <DesktopSidePanelShell
      title="Název a motiv"
      infoText={poemParamInfoTexts.titleMotifs.text}
      onClose={onClose}
    >
      <section>
        <label
          htmlFor={`${inputId}-title`}
          className="block typo-body font-bold"
        >
          Název
        </label>

        <Input
          id={`${inputId}-title`}
          type="text"
          value={title}
          disabled={titleUnset}
          onChange={(event) =>
            updateParams({ title: event.target.value })
          }
          placeholder="Název"
          className={`mt-4 ${inputClassName}`}
        />

        <DesktopUnsetToggle
          label="Název"
          unset={titleUnset}
          onUnsetChange={(unset) => setUnset('title', unset)}
        />
      </section>

      <section className="mt-20">
        <h3 className="typo-body font-bold">
          Motivy
        </h3>

      <div className="mt-4 space-y-4">
        {motifInputs.map((motif, index) => {

          const canAdd =
            index === motifInputs.length - 1 &&
            motifInputs.length < MAX_MOTIFS

          const canRemove =
            !canAdd &&
            (motifInputs.length > 1 || motif.length > 0)

          const actionButtonClassName = [
            'grid size-11 shrink-0 place-items-center',
            'rounded-2xl bg-yellow-300 text-zinc-900',
            'cursor-pointer',
            'focus-visible:outline-none focus-visible:ring-2',
            'focus-visible:ring-white',
            'disabled:cursor-not-allowed',
            'disabled:bg-purple-200/70',
          ].join(' ')

          return (
            <div key={index} className="flex items-center gap-3">
              <Input
                type="text"
                aria-label={`Motiv ${index + 1}`}
                value={motif}
                disabled={motifsUnset}
                onChange={(event) =>
                  updateMotif(index, event.target.value)
                }
                placeholder={
                  motifInputs.length === 1
                    ? 'Motivy'
                    : `Motiv ${index + 1}`
                }
                className={`min-w-0 flex-1 ${inputClassName}`}
              />

              {canRemove && (
                <button
                  type="button"
                  aria-label={`Odstranit motiv ${index + 1}`}
                  title="Odstranit motiv"
                  disabled={motifsUnset}
                  onClick={() => removeMotif(index)}
                  className={actionButtonClassName}
                >
                  <AppIcon name="trash" size={18} />
                </button>
              )}

              {canAdd && (
                <button
                  type="button"
                  aria-label="Přidat motiv"
                  disabled={motifsUnset}
                  onClick={addMotif}
                  className={actionButtonClassName}
                >
                  <Plus size={18} strokeWidth={2.5} />
                </button>
              )}
            </div>
          )
        })}
      </div>

        <DesktopUnsetToggle
          label="Motivy"
          unset={motifsUnset}
          onUnsetChange={(unset) => setUnset('motifs', unset)}
        />
      </section>

      <section className="mt-20">
        <fieldset>
          <legend className="typo-body font-bold">
            Nálada
          </legend>

          <RadioGroup
            disabled={moodUnset}
            value={mood ?? ''}
            onValueChange={(value) =>
              updateParams({ mood: value as PoemMood })
            }
            className="mt-4"
          >
            {MOOD_OPTIONS.map((option) => (
              <label
                key={option.value}
                className={[
                  'flex items-center gap-3 typo-body',
                  moodUnset
                    ? 'cursor-not-allowed text-purple-200/70'
                    : 'cursor-pointer text-white',
                ].join(' ')}
              >
                <RadioGroupItem value={option.value} />

                {option.label}
              </label>
            ))}
          </RadioGroup>
        </fieldset>

        <DesktopUnsetToggle
          label="Nálada"
          unset={moodUnset}
          onUnsetChange={(unset) => setUnset('mood', unset)}
        />
      </section>
    </DesktopSidePanelShell>
  )
}