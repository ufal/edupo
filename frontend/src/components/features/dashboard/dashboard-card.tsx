'use client'

import type { PoemMode } from '@/types/poem'
import { Card } from '@/components/ui/card'
import { PoemAnalysisView } from './poem-views/poem-analysis-view'
import { PoemEditingView } from './poem-views/poem-editing-view'
import { PoemReadingView } from './poem-views/poem-reading-view'

type DashboardCardProps = {
  mode: PoemMode
}

export function DashboardCard({ mode }: DashboardCardProps) {
  return (
    <Card className="flex grow rounded-3xl bg-white px-4 py-5 desktop:min-h-[430px] desktop:px-[40px] desktop:py-[38px]">
      {mode === 'reading' && <PoemReadingView />}
      {mode === 'analysis' && <PoemAnalysisView />}
      {mode === 'editing' && <PoemEditingView />}
    </Card>
  )
}
