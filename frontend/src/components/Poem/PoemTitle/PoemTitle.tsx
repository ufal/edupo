
interface PoemTitleProps {
    authorName: string | null;
    sidePanelControlElement?: React.ReactNode
}

export default function PoemTitle({ authorName, sidePanelControlElement } : PoemTitleProps) {
    return (
        <div className="flex flex-row justify-between items-center bg-silverTransparent rounded-lg px-6">
            <div className="w-full flex flex-row items-baseline py-4 gap-4 text-blackSoft">
                <h1 className="leading-[18px]">
                    { authorName ? "Generovaná báseň" : "" }
                </h1>
                <h3 className="leading-[18px] m-0">
                    { authorName ? authorName : "" }
                </h3>
                <img src="/svg/robot.svg" className="w-5 h-5 relative top-[3px]" />
            </div>
            { sidePanelControlElement }
        </div>
    )
}