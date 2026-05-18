import { usePoem } from "@/store/poemStore";
import RobotIcon from "@/components/ui/RobotIcon";

interface PoemTitleProps {
    sidePanelControlElement?: React.ReactNode
}

export default function PoemTitle({ sidePanelControlElement } : PoemTitleProps) {
    const { currentValues } = usePoem();

    const poemName = currentValues.title ? currentValues.title : "";
    const authorName = currentValues.author ? currentValues.author : "";

    return (
        <div className="flex flex-row justify-between items-center bg-silverTransparent rounded-lg px-6 h-[56px]">
            <div className="w-full flex flex-row items-baseline py-4 gap-4 text-zinc700">
                <h1 className="leading-[18px]">
                    { poemName }
                </h1>
                <h3 className="leading-[18px] m-0">
                    { authorName }
                </h3>
                { authorName && <RobotIcon type="circle" cls="top-[3px]" /> }
            </div>
            { sidePanelControlElement }
        </div>
    )
}