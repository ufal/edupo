'use client'

import { usePoemStore } from '@/stores/poem-store'
import { useDesktopSettingsUiStore } from '@/stores/desktop-settings-ui-store'
import { getAllAuthorStyles } from '@/services/author-styles-service'
import authorCollections from '@/data/author-collections.json'
import { SearchableSelect } from '@/components/ui/searchable-select'
import { DesktopSidePanelShell } from './desktop-side-panel-shell'
import { DesktopParamSetting } from './desktop-param-setting'

type DesktopAuthorStylePanelProps = {
  onClose: () => void
}

const authors = getAllAuthorStyles()

const authorOptions = authors.map((author) => ({
  value: author.id,
  label: author.label,
}))

const collectionOptions = authors.flatMap((author) =>
  authorCollections
    .filter((collection) => collection.authorId === author.id)
    .map((collection) => ({
      value: collection.id,
      label: collection.label,
      group: author.label,
    })),
)

export function DesktopAuthorStylePanel({
  onClose,
}: DesktopAuthorStylePanelProps) {
  const authorId = usePoemStore(
    (state) => state.selectedAuthorStyleId,
  )
  const setSelectedAuthorStyleId = usePoemStore(
    (state) => state.setSelectedAuthorStyleId,
  )

  const authorUnset = useDesktopSettingsUiStore(
    (state) => state.unset.authorStyleId,
  )
  const collectionUnset = useDesktopSettingsUiStore(
    (state) => state.unset.collectionId,
  )

  const collectionId = useDesktopSettingsUiStore(
    (state) => state.selectedCollectionId,
  )
  const setSelectedCollectionId = useDesktopSettingsUiStore(
    (state) => state.setSelectedCollectionId,
  )

  return (
    <DesktopSidePanelShell
      title="Autorský styl"
      infoText="Vyberte autora a případně sbírku, jejichž stylem se má báseň inspirovat."
      onClose={onClose}
    >
      <section>
        <h3 className="typo-body font-bold">
          Autor
        </h3>

        <DesktopParamSetting
          param="authorStyleId"
          label="Autor"
        >
          <SearchableSelect
            className="mt-4"
            label="Autor"
            placeholder="Autor"
            searchPlaceholder="Hledat autora"
            value={authorId}
            options={authorOptions}
            disabled={authorUnset}
            onChange={setSelectedAuthorStyleId}
          />
        </DesktopParamSetting>
      </section>

      <section className="mt-20">
        <h3 className="typo-body font-bold">
          Sbírka
        </h3>

        <DesktopParamSetting
          param="collectionId"
          label="Sbírka"
        >
          <SearchableSelect
            className="mt-4"
            label="Sbírka"
            placeholder="Sbírka"
            searchPlaceholder="Hledat sbírku"
            value={collectionId}
            options={collectionOptions}
            disabled={collectionUnset}
            onChange={setSelectedCollectionId}
          />
        </DesktopParamSetting>
      </section>
    </DesktopSidePanelShell>
  )
}