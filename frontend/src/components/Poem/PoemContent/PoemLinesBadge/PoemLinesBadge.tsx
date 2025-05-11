import { PoemLineColorSchemeName, PoemLineColorSchemes } from "../PoemLineColorSchemes";
import { Pencil1Icon } from "@radix-ui/react-icons";
import { LockKeyholeIcon } from "lucide-react";
import { twMerge } from "tailwind-merge";

export function PoemLinesEditBadge({ onClick, locked } : { onClick: () => void; locked: boolean }) {
    const cls = twMerge("w-[28px] h-[30px] bg-slate300 rounded-full flex items-center justify-center", locked ? "cursor-pointer" : null);

    return (
        <div className="h-[34px] bg-slate200 flex items-center justify-center rounded-l-md">
            <div className={cls} onClick={locked ? onClick : undefined}>
                {
                    locked
                        ? <Pencil1Icon className="text-slate700 w-[20px] h-[20px]" />
                        : <LockKeyholeIcon className="text-slate700 w-[20px] h-[20px]" />
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
        <div className={`h-[26px] bg-${bgBackground} flex items-center justify-center rounded-l-md`}>
            <div className={`w-[28px] h-[22px] bg-${bgForeground} rounded-full flex items-center justify-center`}>
                <div className={`text-${textColor} text-[14px] font-bold`}>
                    {letter}
                </div>
            </div>
        </div>
    )
}