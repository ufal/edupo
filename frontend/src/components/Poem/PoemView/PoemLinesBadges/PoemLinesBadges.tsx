import { PoemLineColorSchemeName, PoemLineColorSchemes } from "../PoemLineColorSchemes";
import RobotIcon from "@/components/ui/RobotIcon";
import { Pencil1Icon } from "@radix-ui/react-icons";
import { LockKeyholeIcon } from "lucide-react";
import { twMerge } from "tailwind-merge";

export function PoemEditedBadge() {
    return (
        <div className={`h-[24px] bg-white flex items-center justify-center gap-[8px] rounded-md text-sky500 border-sky200 border px-[10px] py-[4px]`}>
            <RobotIcon type="square" />
            <div className="text-[12px]">
                Upraveno
            </div>
        </div>
    )
}

export function PoemLockedBadge() {
    return (
        <div className={``}>
            <LockKeyholeIcon className="text-slate400 w-[20px] h-[20px]" />
        </div>
    )
}

export function PoemLinesLockedBadge({ onClick, locked } : { onClick: () => void; locked: boolean }) {
    const cls = twMerge("w-[30px] h-[30px] flex items-center justify-center", locked ? "cursor-pointer bg-slate300 rounded-full" : null);

    return (
        <div className={twMerge("h-[40px] bg-slate200 flex items-center justify-center rounded-l-md", locked ? "" : "")}>
            <div className={cls} onClick={locked ? onClick : undefined}>
                {
                    locked
                        ? <Pencil1Icon className="text-slate700 w-[20px] h-[20px]" />
                        : <LockKeyholeIcon className="text-slate400 w-[20px] h-[20px]" />
                }
            </div>
        </div>
    )
}

export function PoemLinesLetterBadge({ letter, poemLineColorScheme } : { letter: string, poemLineColorScheme: PoemLineColorSchemeName }) {

    const scheme = PoemLineColorSchemes[poemLineColorScheme];
    const bgBackground = scheme.background;
    const bgForeground = scheme.foreground;
    const textColor = scheme.text;

    return (
        <div className={`h-[40px] bg-${bgBackground} flex items-center justify-center rounded-l-md`}>
            <div className={`w-[28px] h-[22px] bg-${bgForeground} rounded-full flex items-center justify-center`}>
                <div className={`text-${textColor} text-[14px] font-bold`}>
                    {letter}
                </div>
            </div>
        </div>
    )
}