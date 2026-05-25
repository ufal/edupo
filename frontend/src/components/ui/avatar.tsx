'use client'

import { useState } from 'react'
import Image from 'next/image'

const FALLBACK_AVATAR_SRC = "assets/author-avatar.svg"

type AvatarProps = {
  src?: string | null
  alt?: string
  size?: number
}

export function Avatar({
  src,
  alt = 'Author',
  size = 120,
}: AvatarProps) {
  const avatarSrc = src ?? FALLBACK_AVATAR_SRC
  const [currentSrc, setCurrentSrc] = useState(avatarSrc)

  if (currentSrc !== avatarSrc) {
    setCurrentSrc(avatarSrc)
  }

  return (
    <Image
      src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + currentSrc}
      alt={alt}
      width={size}
      height={size}
      style={{ width: `${size}px`, height: `${size}px` }}
      onError={() => setCurrentSrc(FALLBACK_AVATAR_SRC)}
      priority
    />
  )
}