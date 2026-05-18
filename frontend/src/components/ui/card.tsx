type CardProps = {
  children: React.ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={`rounded-2xl bg-neutral-100 p-4 ${className || ''}`}>
      {children}
    </div>
  )
}