import Image from 'next/image'

const base = process.env.NEXT_PUBLIC_LINK_BASE || '/'

type PartnerLogosVariant = 'vertical' | 'horizontal'
type PartnerLogosSet = 'full' | 'reduced'
type PartnerLogosColor = 'white' | 'gray'

type LogoItem = {
  src: string
  alt: string
  width: number
  height: number
}

const logoSets: Record<PartnerLogosSet, LogoItem[]> = {
  full: [
    { src: 'assets/logos/logo-tacr.svg', alt: 'TA ČR', width: 38, height: 38 },
    { src: 'assets/logos/logo-ucl.svg', alt: 'Ústav české literatury AV ČR', width: 116, height: 54 },
    { src: 'assets/logos/logo-vsvu.svg', alt: 'VŠVU Bratislava', width: 102, height: 41 },
    { src: 'assets/logos/logo-didaktikon.svg', alt: 'Didaktikon', width: 60, height: 60 },
    { src: 'assets/logos/logo-matfyz.svg', alt: 'Matfyz', width: 87, height: 38 },
  ],
  reduced: [
    { src: 'assets/logos/logo-uk.svg', alt: 'Univerzita Karlova', width: 38, height: 32 },
    { src: 'assets/logos/logo-ucl-sm.svg', alt: 'Ústav české literatury AV ČR', width: 34, height: 27 },
  ],
}

type PartnerLogosProps = {
  variant: PartnerLogosVariant
  set?: PartnerLogosSet
  color?: PartnerLogosColor
  className?: string
}

export function PartnerLogos({
  variant,
  set = 'full',
  color = 'white',
  className = '',
}: PartnerLogosProps) {
  const layoutClassName =
    variant === 'horizontal'
      ? 'flex flex-row gap-10' + (set === 'full' ? ' items-center' : ' items-end')
      : 'flex flex-col items-center gap-16 justify-between' 

  return (
    <div className={[layoutClassName, className].join(' ')}>
      {logoSets[set].map((logo) => {

        const src =
          set === 'reduced' && color === 'gray'
            ? `${base}${logo.src.replace('.svg', '-gray.svg')}`
            : `${base}${logo.src}`

        return <Image
          key={logo.src}
          src={src}
          alt={logo.alt}
          width={logo.width}
          height={logo.height}
          priority
        />

      })}
    </div>
  )
}