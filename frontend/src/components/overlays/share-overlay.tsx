'use client'

import { useEffect, useState } from 'react'
import { QRCodeSVG } from 'qrcode.react'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { AppIcon } from '../icons/app-icon'
import { ShellOverlay } from './shell-overlay'
import { ShellControlPanel } from './shell-control-panel'
import { DesktopModalOverlay } from './desktop-modal-overlay'

export function ShareOverlay({ onClose }: { onClose: () => void }) {
  const [url, setUrl] = useState('')

  useEffect(() => {
    setUrl(window.location.href)
  }, [])

  const copyUrl = async () => {
    if (!url) return

    await navigator.clipboard.writeText(url)
    toast.success('Odkaz byl zkopírován')
  }

  const shareFacebook = () => {
    if (!url) return

    window.open(
      `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
      '_blank',
      'noopener,noreferrer',
    )
  }

  const shareX = () => {
    if (!url) return

    window.open(
      `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}`,
      '_blank',
      'noopener,noreferrer',
    )
  }

  const shareLinkedIn = () => {
    if (!url) return

    window.open(
      `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
      '_blank',
      'noopener,noreferrer',
    )
  }

  const content = (
    <div className="flex flex-col items-center rounded-3xl bg-white px-6 py-8 desktop:w-[476px] desktop:px-10 desktop:py-[66px]">
      {url && (
        <QRCodeSVG
          value={url}
          size={180}
          bgColor="#ffffff"
          fgColor="#111827"
          level="M"
        />
      )}

      <Button
        type="button"
        variant="primary"
        size="md"
        className="mt-7 px-10 desktop:mt-[60px]"
        onClick={copyUrl}
      >
        Zkopírovat odkaz
      </Button>

      <div className="mt-7 flex items-center justify-center gap-10 desktop:mt-9">
        <button
          type="button"
          onClick={shareFacebook}
          className="flex flex-col items-center gap-2 text-zinc-500 cursor-pointer"
        >
          <span className="grid size-10 place-items-center rounded-2xl bg-teal-700 text-white">
            <AppIcon name="fb" size={22} className="text-white" />
          </span>
          <span className="text-xs">Facebook</span>
        </button>

        <button
          type="button"
          onClick={shareX}
          className="flex flex-col items-center gap-2 text-zinc-500 cursor-pointer"
        >
          <span className="grid size-10 place-items-center rounded-2xl bg-teal-700 text-white">
            <AppIcon name="x" size={16} className="text-white" />
          </span>
          <span className="text-xs">X</span>
        </button>

        <button
          type="button"
          onClick={shareLinkedIn}
          className="flex flex-col items-center gap-2 text-zinc-500 cursor-pointer"
        >
          <span className="grid size-10 place-items-center rounded-2xl bg-teal-700 text-white">
            <AppIcon name="linkedIn" size={22} className="text-white" />
          </span>
          <span className="text-xs">LinkedIn</span>
        </button>
      </div>
    </div>
  )

  return (
    <>
      <div className="block desktop:hidden">
        <ShellOverlay variant="menu" className="bg-yellow-50">
          <ShellControlPanel
            iconName="qr"
            title="Sdílení básně"
            onClose={onClose}
          />

          <div className="px-5 pt-9">{content}</div>
        </ShellOverlay>
      </div>

      <DesktopModalOverlay onClose={onClose}>{content}</DesktopModalOverlay>
    </>
  )
}