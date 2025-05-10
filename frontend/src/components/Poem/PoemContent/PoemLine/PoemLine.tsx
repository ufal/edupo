import { PoemLineColorScheme } from "../PoemLineColorSchemes";
import { Input } from "@/components/ui/input";
import { twMerge } from "tailwind-merge";

export default function PoemLine({ text, colorScheme, isEditable} : { text: string; colorScheme?: PoemLineColorScheme; isEditable?: boolean }) {
    let cls = "px-10 flex items-center";

    if (colorScheme)
        cls = twMerge(cls, `bg-${colorScheme.backgroundTransparent}`);

    if (isEditable)
        cls = twMerge(cls, "h-[34px] bg-slate200Transparent");
    else
        cls = twMerge(cls, "h-[26px]");
    
    return (
        <div className={cls}>
            {
                (isEditable)
                    ? <Input type="text" className="h-[30px] py-1 px-2 bg-slate100 border-slate200 md:text-[16px]" value={text} disabled />
                    : text
            }
        </div>
    )
}