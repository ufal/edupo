import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { DesktopHeader } from '@/components/layout/desktop/desktop-header'

type DesktopWelcomeScreenProps = {
  onContinue: () => void
}

export function DesktopWelcomeScreen({ onContinue }: DesktopWelcomeScreenProps) {
  return (
    <div className="fixed inset-0 flex flex-col bg-primary text-primary-foreground">
      <DesktopHeader />

      <main className="flex flex-1 flex-col items-center justify-center text-center">
        <section className="flex flex-col items-center">
          <h2 className="typo-h2 mb-16">
            Vytvořte si svou jedinečnou báseň
          </h2>

          <Image
            src={(process.env.NEXT_PUBLIC_LINK_BASE || '/') + 'assets/girl-with-computer.svg'}
            alt=""
            width={374}
            height={337}
            style={{ width: '374px', height: '337px' }}
            priority
          />

          <p className="typo-large max-w-[720px]">
            Nastavte autora, styl a motivy podle svých představ. AI vytvoří báseň přesně pro vás.
          </p>

          <Button
            variant="subtle"
            size="md"
            onClick={onContinue}
            className="mt-8"
          >
            Pokračovat
          </Button>
        </section>
      </main>
    </div>
  )
}