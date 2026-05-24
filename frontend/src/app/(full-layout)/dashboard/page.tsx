'use client'

import { Suspense, useEffect, useRef } from 'react'
import { useSearchParams } from 'next/navigation'

import { DashboardScreen } from '@/components/features/dashboard/dashboard-screen'
import { usePoemStore } from '@/stores/poem-store'
import { isPoemMode } from '@/types/poem'

export default function DashboardPage() {
  return (
    <Suspense fallback={null}>
      <DashboardPageContent />
    </Suspense>
  )
}

function DashboardPageContent() {
  const searchParams = useSearchParams()

  const poemId = searchParams.get('poemId')
  const viewMode = searchParams.get('viewMode')

  const poem = usePoemStore((state) => state.poem)
  const setMode = usePoemStore((state) => state.setMode)
  const loadPoemById = usePoemStore((state) => state.loadPoemById)

  const didApplyViewMode = useRef(false)

  useEffect(() => {
    if (didApplyViewMode.current) return
    if (!isPoemMode(viewMode)) return

    setMode(viewMode)
    didApplyViewMode.current = true
  }, [viewMode, setMode])

  useEffect(() => {
    if (!poemId) return
    if (poem?.id === poemId) return

    void loadPoemById(poemId)
  }, [poemId, poem?.id, loadPoemById])

  return <DashboardScreen />
}