import { twMerge } from 'tailwind-merge'

export default function Sidebar({ cls, children } : { cls?: string; children: React.ReactNode }) {
  return (
    <div className={twMerge("w-[482px] bg-white border-l", cls)}>
      {
        children
      }
    </div>
  )
}