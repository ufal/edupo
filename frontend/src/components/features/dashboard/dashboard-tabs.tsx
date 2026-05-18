import type { PoemMode } from '@/types/poem'

type DashboardTabsProps = {
  value: PoemMode
  onChange: (value: PoemMode) => void
}

const selectedClass = 'underline text-purple-500'
const defaultClass = 'text-foreground'

export function DashboardTabs({ value, onChange }: DashboardTabsProps) {
  return (
    <div className="flex gap-8 rounded-2xl bg-white p-4 typo-large">
      <button
        type="button"
        onClick={() => onChange('reading')}
        className={value === 'reading' ? selectedClass : defaultClass}
      >
        Četba
      </button>

      <button
        type="button"
        onClick={() => onChange('analysis')}
        className={value === 'analysis' ? selectedClass : defaultClass}
      >
        Analýza
      </button>

      <button
        type="button"
        onClick={() => onChange('editing')}
        className={value === 'editing' ? selectedClass : defaultClass}
      >
        Úprava textu
      </button>
    </div>
  )
}