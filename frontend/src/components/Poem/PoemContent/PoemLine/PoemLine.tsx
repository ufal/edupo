import { PoemLineColorScheme } from "../PoemLineColorSchemes";
import { Input } from "@/components/ui/input";
import { twMerge } from "tailwind-merge";
import { Trash2Icon } from "lucide-react";

interface PoemLineProps {
    text: string;
    colorScheme?: PoemLineColorScheme;
    isEditable?: boolean;
    locked?: boolean;
    onChange?: (newText: string) => void;
    onClear?: () => void;
}

export default function PoemLine({ text, colorScheme, isEditable, locked, onChange, onClear} : PoemLineProps) {
    let cls = "px-10 py-[2px]";

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
                    ? (
                        <div className="flex gap-1">
                            <Input
                                type="text"
                                className="h-[30px] py-1 px-2 bg-slate100 border-slate200 md:text-[16px] focus-visible:ring-0 flex-1"
                                value={text}
                                disabled={locked}
                                onChange={(e) => onChange?.(e.target.value)} />
                            <div
                                className={twMerge("w-[30px] h-[30px] flex items-center justify-center shrink-0", !locked ? "bg-red200 rounded-full cursor-pointer" : null)}
                                onClick={onClear}>
                                {
                                    !locked && <Trash2Icon className="w-[20px] h-[20px] text-red700" />
                                }
                            </div>
                        </div>
                    )
                    : text
            }
        </div>
    )
}