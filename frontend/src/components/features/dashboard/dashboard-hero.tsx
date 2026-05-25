'use client'

import { Avatar } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'
import { getAuthorStyleById } from '@/services/author-styles-service'

export function DashboardHero() {
  const selectedAuthorStyleId = usePoemStore(
    (state) => state.selectedAuthorStyleId,
  )

  const openOverlay = useUiStore((state) => state.openOverlay)

  const selectedAuthor = getAuthorStyleById(selectedAuthorStyleId)

  return (
    <section className="flex items-center gap-5 rounded-3xl bg-white px-4 py-4">
      <div className="shrink-0">
        <Avatar
          src={selectedAuthor?.avatarSrc}
          alt={selectedAuthor?.label ?? 'Author'}
          size={120}
        />
      </div>

      {selectedAuthor && (
        <div className="flex min-w-0 flex-1 flex-col items-center gap-3">
          <h2 className="max-w-full truncate text-center typo-large text-foreground">
            {selectedAuthor.label}
          </h2>

          <div className="flex w-full flex-col gap-2">
            <Button
              type="button"
              variant="primary"
              size="sm"
              className="w-full"
              onClick={() => openOverlay('author-style')}
            >
              Změnit styl podle autora
            </Button>

            <Button
              type="button"
              variant="primary"
              size="sm"
              className="w-full"
            >
              Vyplnit náhodně
            </Button>
          </div>
        </div>
      )}
    </section>
  )
}