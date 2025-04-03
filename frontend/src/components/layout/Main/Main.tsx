export default function Main({ cls, children } : { cls?: string; children: React.ReactNode }) {
  return (
    <main className={"w-full " + cls}>
      {
        children
      }
    </main>
  )
}