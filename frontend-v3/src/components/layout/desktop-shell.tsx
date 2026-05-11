import type { ReactNode } from 'react'

type DesktopShellProps = {
  children: ReactNode
}

export function DesktopShell({ children }: DesktopShellProps) {
  return (
    <div className="min-h-screen bg-white text-black desktop:grid desktop:grid-cols-[280px_1fr]">
      <aside className="border-r border-neutral-200 p-6">
        <div className="text-large">Edupo</div>
      </aside>

      <div className="min-w-0">
        <header className="border-b border-neutral-200 px-8 py-5">
          <div className="text-large">Desktop layout</div>
        </header>

        <main className="px-8 py-6">
          {children}
        </main>
      </div>
    </div>
  )
}