export default function PoemTitle({ text, value } : { text: string; value?: string }) {
    return (
        <div className="text-sm pb-[8px]">
            <span className="font-normal">
                { text }
            </span>
            {
                value ? <span className="font-light pl-[12px] text-graySoft">{value}</span> : null
            }
        </div>
    )
}