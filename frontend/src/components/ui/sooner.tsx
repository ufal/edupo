'use client'

import { Toaster } from 'sonner'

export function AppToaster() {
  return (
    <Toaster
      position="top-center"
      richColors
      toastOptions={{
        className:
          '!rounded-2xl !border-0 !shadow-lg',
      }}
    />
  )
}