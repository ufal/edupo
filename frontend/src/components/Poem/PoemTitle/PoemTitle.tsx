import { usePoem } from "@/store/poemStore";

interface PoemTitleProps {
    sidePanelControlElement?: React.ReactNode
}

export default function PoemTitle({ sidePanelControlElement } : PoemTitleProps) {
    const { currentValues } = usePoem();

    const poemName = currentValues.title ? currentValues.title : "";
    const authorName = currentValues.author ? currentValues.author : "";

    return (
        <div className="flex flex-row justify-between items-center bg-silverTransparent rounded-lg px-6 h-[56px]">
            <div className="w-full flex flex-row items-baseline py-4 gap-4 text-blackSoft">
                <h1 className="leading-[18px]">
                    { poemName }
                </h1>
                <h3 className="leading-[18px] m-0">
                    { authorName }
                </h3>
                { authorName && <img src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "svg/robot.svg"} className="w-5 h-5 relative top-[3px]" /> }
            </div>
            { sidePanelControlElement }
        </div>
    )
}