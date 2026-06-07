'use client'

import { Avatar } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'
import {
  getAllAuthorStyles,
  getAuthorStyleById,
} from '@/services/author-styles-service'

export function DashboardHero() {
  const selectedAuthorStyleId = usePoemStore(
    (state) => state.selectedAuthorStyleId,
  )
  const setSelectedAuthorStyleId = usePoemStore(
    (state) => state.setSelectedAuthorStyleId,
  )

  const openOverlay = useUiStore((state) => state.openOverlay)
  const selectedAuthor = getAuthorStyleById(selectedAuthorStyleId)

  const fillRandomAuthorStyle = () => {
    const styles = getAllAuthorStyles()
    const randomStyle = styles[Math.floor(Math.random() * styles.length)]

    if (randomStyle) {
      setSelectedAuthorStyleId(randomStyle.id)
    }
  }

  return (
    <section className="flex items-center gap-5 rounded-3xl bg-white px-4 py-4 desktop:min-h-[212px] desktop:gap-[60px] desktop:px-[30px] desktop:py-[28px]">
      <div className="shrink-0 desktop:[&>img]:h-[154px] desktop:[&>img]:w-[154px]">
        <Avatar
          src={selectedAuthor?.avatarSrc}
          alt={selectedAuthor?.label ?? 'Author'}
          size={120}
        />
      </div>

      <div className="flex min-w-0 flex-1 flex-col items-center gap-3 desktop:max-w-[232px]">
        <h2 className="max-w-full truncate text-center typo-large text-foreground">
          {selectedAuthor?.label ?? 'Vyber styl autora'}
        </h2>

        <div className="flex w-full flex-col gap-2 desktop:gap-3">
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
            onClick={fillRandomAuthorStyle}
          >
            Vyplnit náhodně
          </Button>
        </div>
      </div>
    </section>
  )
}