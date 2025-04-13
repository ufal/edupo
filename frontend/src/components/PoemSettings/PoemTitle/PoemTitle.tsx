export default function PoemTitle({ text } : { text: string }) {
    return (
        <div className="text-sm font-normal pb-[8px]">
            { text }
        </div>
    )
}