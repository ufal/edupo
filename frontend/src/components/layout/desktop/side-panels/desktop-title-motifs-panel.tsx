'use client'

import { useState } from 'react'
import { Plus } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { usePoemStore } from '@/stores/poem-store'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { poemParamInfoTexts } from '@/config/poem-param-info-texts'
import { MAX_MOTIFS } from '@/config/poem-param-title-motifs'

const EMPTY_MOTIFS: string[] = []

type DesktopTitleMotifsPanelProps = {
  onClose: () => void
}

export function DesktopTitleMotifsPanel({ onClose }: DesktopTitleMotifsPanelProps) {
  const title = usePoemStore((state) => state.params.title ?? '')
  const motifs = usePoemStore((state) => state.params.motifs ?? EMPTY_MOTIFS)
  const updateParams = usePoemStore((state) => state.updateParams)

  const [motifInputs, setMotifInputs] = useState<string[]>(
    motifs.length > 0 ? motifs : [''],
  )

  const cleanMotifs = (values: string[]) =>
    values.map((value) => value.trim()).filter(Boolean)

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

  return (
    <DesktopSidePanelShell onClose={onClose} title={poemParamInfoTexts.titleMotifs.title} infoText={poemParamInfoTexts.titleMotifs.text}>
      <section>
        
        <label className="typo-body font-bold">
          Název
        </label>

        <Input
          type="text"
          value={title}
          onChange={(event) => updateParams({ title: event.target.value })}
          placeholder="Název"
          className="mt-4"
        />
      </section>

      <section className="mt-20">
        <label className="typo-body font-bold">
          Motivy
        </label>

        <div className="mt-4 space-y-4">
          {motifInputs.map((motif, index) => {
            const isLast = index === motifInputs.length - 1
            const canAddMotif = motifInputs.length < MAX_MOTIFS

            return (
              <div key={index} className="flex items-center gap-3">
                <Input
                  type="text"
                  value={motif}
                  onChange={(event) => updateMotif(index, event.target.value)}
                  placeholder={`Motiv ${index + 1}`}
                  className="min-w-0 flex-1"
                />

                {isLast && canAddMotif && (
                  <button
                    type="button"
                    aria-label="Přidat motiv"
                    onClick={addMotif}
                    className="grid size-11 shrink-0 place-items-center rounded-2xl bg-yellow-300 text-zinc-900 cursor-pointer"
                  >
                    <Plus size={18} strokeWidth={2.5} />
                  </button>
                )}
              </div>
            )
          })}
        </div>
      </section>
    </DesktopSidePanelShell>
  )
}