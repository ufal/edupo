import { X, InfoIcon } from 'lucide-react'
import { AppIcon } from '@/components/icons/app-icon'
import { Button } from '@/components/ui/button'

type InfoPopupMode = 'overlay' | 'inline'

type InfoPopupProps = {
  text: string
  onClose: () => void
  mode?: InfoPopupMode
}

export function InfoPopup({
  text,
  onClose,
  mode = 'overlay',
}: InfoPopupProps) {
  const isOverlay = mode === 'overlay'

  return (
    <div
      className={
        isOverlay
          ? 'fixed inset-0 z-100 flex items-center justify-center bg-purple-500/90 px-6'
          : 'flex w-full justify-center'
      }
    >
      {isOverlay && (
        <button
          type="button"
          aria-label="Zavřít nápovědu"
          onClick={onClose}
          className="absolute right-6 top-56 grid size-8 place-items-center text-white"
        >
          <X size={28} strokeWidth={2.2} />
        </button>
      )}

      <div className="flex w-full max-w-[220px] flex-col items-center gap-5 rounded-3xl bg-white px-7 py-6 text-center text-grey-900">
        <InfoIcon size={36} className="text-grey-900" />

        <p className="typo-small text-grey-900">
          {text}
        </p>

        <Button
          type="button"
          variant="primary"
          size="sm"
          className="w-full"
          onClick={onClose}
        >
          Zavřít
        </Button>
      </div>
    </div>
  )
}