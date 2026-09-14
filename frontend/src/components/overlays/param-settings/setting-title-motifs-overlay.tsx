'use client'

import { useState } from 'react'
import { Plus } from 'lucide-react'
import { ShellOverlay } from '../shell-overlay'
import { ShellControlPanel } from '../shell-control-panel'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { MAX_MOTIFS } from '@/config/poem-param-title-motifs'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { MOOD_OPTIONS } from '@/config/poem-param-mood'
import type { PoemMood } from '@/types/poem'

const EMPTY_MOTIFS: string[] = []

export function SettingTitleMotifsOverlay({
  onClose,
}: {
  onClose: () => void
}) {
  const title = usePoemStore((state) => state.params.title ?? '')
  const motifs = usePoemStore(
    (state) => state.params.motifs ?? EMPTY_MOTIFS,
  )
  const mood = usePoemStore((state) => state.params.mood)
  const updateParams = usePoemStore((state) => state.updateParams)

  const [motifInputs, setMotifInputs] = useState<string[]>(
    motifs.length > 0 ? motifs : [''],
  )

  const cleanMotifs = (values: string[]) =>
    values.map((value) => value.trim()).filter(Boolean)

  const updateTitle = (value: string) => {
    updateParams({ title: value })
  }

  const updateMotif = (index: number, value: string) => {
    const nextMotifInputs = [...motifInputs]
    nextMotifInputs[index] = value

    setMotifInputs(nextMotifInputs)
    updateParams({ motifs: cleanMotifs(nextMotifInputs) })
  }

  const addMotif = () => {
    if (motifInputs.length >= MAX_MOTIFS) return
    setMotifInputs([...motifInputs, ''])
  }

  const canAddMotif = motifInputs.length < MAX_MOTIFS

  return (
    <ShellOverlay variant="menu" className="bg-yellow-50">
      <ShellControlPanel
        iconName="book"
        title={poemParamInfoTexts.titleMotifs.title}
        onClose={onClose}
        infoText={poemParamInfoTexts.titleMotifs.text}
      />

      <div className="px-5 pt-8">
        <section>
          <label className="typo-large text-grey-700">
            Název
          </label>

          <Input
            type="text"
            value={title}
            onChange={(event) => updateTitle(event.target.value)}
            placeholder="Název"
            className="mt-2"
          />
        </section>

        <section className="mt-9">
          <label className="typo-large text-grey-700">
            Motivy
          </label>

          <div className="mt-2 space-y-3">
            {motifInputs.map((motif, index) => {
              const isLast = index === motifInputs.length - 1
              const showAddButton = isLast && canAddMotif

              return (
                <div key={index} className="flex items-center gap-3">
                  <Input
                    type="text"
                    value={motif}
                    onChange={(event) =>
                      updateMotif(index, event.target.value)
                    }
                    placeholder={`Motiv ${index + 1}`}
                    className="min-w-0 flex-1"
                  />

                  {showAddButton && (
                    <button
                      type="button"
                      aria-label="Přidat motiv"
                      onClick={addMotif}
                      className="grid size-11 shrink-0 place-items-center rounded-2xl bg-teal-700 text-white"
                    >
                      <Plus size={24} strokeWidth={2.5} />
                    </button>
                  )}
                </div>
              )
            })}
          </div>
        </section>

        <section className="mt-10">
          <label className="typo-body font-semibold text-grey-900">
            Nálada
          </label>

          <RadioGroup
            value={mood}
            onValueChange={(value) => {
              updateParams({ mood: value as PoemMood })
            }}
            className="mt-5"
          >
            {MOOD_OPTIONS.map((option) => (
              <label
                key={option.value}
                className="flex cursor-pointer items-center gap-3"
              >
                <RadioGroupItem value={option.value} />

                <span className="typo-body text-grey-900">
                  {option.label}
                </span>
              </label>
            ))}
          </RadioGroup>
        </section>

      </div>
    </ShellOverlay>
  )
}