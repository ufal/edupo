import Image from 'next/image'

export function EdupoLogo() {
  return (
    <Image
      src="/assets/logos/logo-edupo.svg"
      alt="Edupo"
      width={91}
      height={22}
      style={{ width: '91px', height: '22px' }}
      priority
    />
  )
}