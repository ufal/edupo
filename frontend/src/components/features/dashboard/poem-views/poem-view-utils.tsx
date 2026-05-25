import Image from 'next/image'
import type { Poem, PoemLine } from '@/types/poem'
import { useEffect, useRef, useState } from 'react'
import { fetchTTSApi } from '@/services/api/edupo-api'
import { API_BASE_URL } from '@/services/api/http-client'
import { usePoemStore } from '@/stores/poem-store'
import { useUiStore } from '@/stores/ui-store'

export function getPoemLines(poem: Poem | null): PoemLine[] {
  if (!poem) return []

  if (poem.lines?.length) return poem.lines

  return poem.text
    .split('\n')
    .map((text) => text.trim())
    .filter(Boolean)
    .map((text, index) => ({
      id: `line-${index + 1}`,
      text,
    }))
}

export function PoemEmptyState() {
  return (
    <div className="flex flex-col">
      <h2 className="typo-large text-zinc-700">
        Vytvořte si svou jedinečnou báseň
      </h2>

      <div className="mt-5 typo-detail leading-6 text-zinc-700">
        <p>
          Krok za krokem si nastavíte všechny detaily a AI vytvoří báseň podle vašich představ.
        </p>

        <p className="mt-4">
          Začněte výběrem stylu autora a pokračujte nastavením v dolním menu.
        </p>
      </div>
    </div>
  )
}

export function PoemCardActions() {
  const poem = usePoemStore((state) => state.poem)
  const likedPoemIds = usePoemStore((state) => state.likedPoemIds)
  const likingPoemIds = usePoemStore((state) => state.likingPoemIds)
  const likePoem = usePoemStore((state) => state.likePoem)

  const openOverlay = useUiStore((state) => state.openOverlay)

  const isLiked = poem ? Boolean(likedPoemIds[poem.id]) : false
  const isLiking = poem ? Boolean(likingPoemIds[poem.id]) : false
  const isLikeDisabled = !poem || isLiked || isLiking

  const audioRef = useRef<HTMLAudioElement | null>(null)
  const [ttsStatus, setTtsStatus] = useState<'idle' | 'loading' | 'playing' | 'paused'>('idle')

  useEffect(() => {
    return () => {
      audioRef.current?.pause()
      audioRef.current = null
    }
  }, [])

  const img = (src: string, className?: string) => (
    <Image
      src={src}
      alt=""
      width={23}
      height={23}
      className={className}
      style={{ width: 'auto', height: 'auto' }}
    />
  )

  const getAudioUrl = (url: string) => {
    if (url.startsWith('http')) return url

    return new URL(url, API_BASE_URL).toString()
  }

  const handleToggleTTS = async () => {
    if (!poem || ttsStatus === 'loading') return

    if (ttsStatus === 'playing') {
      audioRef.current?.pause()
      setTtsStatus('paused')
      return
    }

    if (ttsStatus === 'paused') {
      try {
        await audioRef.current?.play()
        setTtsStatus('playing')
      } catch (error) {
        console.error(error)
        setTtsStatus('idle')
      }

      return
    }

    setTtsStatus('loading')

    try {
      const URL_PREFIX = 'https://quest.ms.mff.cuni.cz/edupo-api' // TODO: remove

      const response = await fetchTTSApi(poem.id)
      const audio = new Audio(getAudioUrl(URL_PREFIX + response.url))

      audioRef.current = audio

      audio.addEventListener('ended', () => {
        audioRef.current = null
        setTtsStatus('idle')
      })

      audio.addEventListener('error', () => {
        audioRef.current = null
        setTtsStatus('idle')
      })

      await audio.play()

      setTtsStatus('playing')
    } catch (error) {
      console.error(error)

      audioRef.current = null
      setTtsStatus('idle')
    }
  }

  return (
    <div className="mt-auto flex items-center justify-start gap-2 pt-7">
      <button
        type="button"
        aria-label={isLiked ? 'Báseň se mi líbí' : 'Líbí se mi'}
        disabled={isLikeDisabled}
        className={[
          'grid size-8 place-items-center rounded-full transition-transform duration-200',
          isLiked ? 'scale-110 cursor-default' : 'hover:scale-110 active:scale-95',
          isLiking ? 'animate-pulse' : '',
          isLikeDisabled && !isLiked ? 'opacity-50' : '',
        ].join(' ')}
        onClick={() => {
          if (!poem) return
          void likePoem(poem.id)
        }}
      >
        {img(
          (process.env.NEXT_PUBLIC_LINK_BASE || "/") + (isLiked ? "assets/icons/heart-full.svg" : "assets/icons/heart.svg"),
          isLiked ? 'animate-[heart-pop_220ms_ease-out]' : undefined,
        )}
      </button>

      <button
        type="button"
        aria-label="Sdílet"
        className="grid size-8 place-items-center"
        onClick={() => openOverlay('share')}
      >
        {img((process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/icons/share.svg")}
      </button>

      <button
        type="button"
        aria-label={
          ttsStatus === 'playing'
            ? 'Pozastavit přehrávání'
            : 'Přehrát báseň'
        }
        disabled={!poem || ttsStatus === 'loading'}
        className={[
          'ml-auto grid size-8 place-items-center rounded-full transition-transform active:scale-95',
          ttsStatus === 'loading' ? 'animate-pulse opacity-70' : '',
          ttsStatus === 'playing' ? 'bg-grey-200 text-grey-900' : '',
          !poem ? 'opacity-50' : '',
        ].join(' ')}
        onClick={handleToggleTTS}
      >
        {ttsStatus === 'playing' ? (
          <div className="flex items-center gap-[3px]">
            <span className="block h-3.5 w-[3px] rounded-full bg-grey-900" />
            <span className="block h-3.5 w-[3px] rounded-full bg-grey-900" />
          </div>
        ) : (
          img((process.env.NEXT_PUBLIC_LINK_BASE || "/") + "assets/icons/loudspeaker.svg")
        )}
      </button>
    </div>
  )
}