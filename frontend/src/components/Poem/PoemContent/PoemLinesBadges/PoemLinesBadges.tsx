import { PoemGenResult } from "@/types/poemGenResult";
import { PoemLineColorSchemeName, PoemLineColorSchemes } from "../PoemLineColorSchemes";
import { SchemeToColorMappings } from "../SchemeToColorMappings";
import { Pencil1Icon } from "@radix-ui/react-icons";

function EditBadge() {
    return (
        <div className={`h-[34px] bg-slate200 flex items-center justify-center rounded-l-md`}>
            <div className={`w-[28px] h-[30px] bg-slate300 rounded-full flex items-center justify-center`}>
                <Pencil1Icon className="text-slate700 w-[20px] h-[20px]" />
            </div>
        </div>
    )
}

function LetterBadge({ letter, poemLineColorScheme } : { letter: string, poemLineColorScheme: PoemLineColorSchemeName }) {

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

type PoelLinesBadgeType = "letter" | "editIcon";

interface PoemLinesBadgesProps {
    poemGenResult: PoemGenResult;
    type: PoelLinesBadgeType;
}

export default function PoemLinesBadges({ poemGenResult, type } : PoemLinesBadgesProps) {
    
    if (poemGenResult.poemLines == null || poemGenResult.rhymeScheme == null || poemGenResult.poemLines?.length != poemGenResult.rhymeScheme?.length)
        return null;

    console.log(poemGenResult);
    return (
        <div className="w-[34px] py-6 leading-relaxed whitespace-pre-line font-[14px]">
            {
                poemGenResult.poemLines && (
                    <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                        {
                            poemGenResult.poemLines.map((line, i) => {
                                if (type === "editIcon")
                                    return <EditBadge key={i} />;

                                if (type === "letter") {
                                    const letter = poemGenResult.rhymeScheme![i];
                                    const colorScheme = SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings];
    
                                    return <LetterBadge key={i} letter={letter} poemLineColorScheme={colorScheme} />;
                                }
                            })
                        }
                    </div>
                )
            }
        </div>
    )
}