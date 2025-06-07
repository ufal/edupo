import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { PoemLinesEditBadge, PoemLinesLetterBadge } from "./PoemLinesBadge";
import PoemLine from "./PoemLine/PoemLine";
import { SchemeToColorMappings } from "./SchemeToColorMappings";
import { PoemLineColorSchemes } from "./PoemLineColorSchemes";
import { usePoem } from "@/store/poemStore";


const ErrorText = (msg: string) => <p className="text-crimsonRed px-10">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft px-10">Načítám báseň...</p>;

type PoemContentLinesMode = "plaintext" | "highlighted" | "editable";

export default function PoemContent({ linesMode } : { linesMode: PoemContentLinesMode }) {
    const [unlockedLines, setUnlockedLines] = useState<number[]>([]);
    const { draftValues, setDraftParam, poemLoading, poemError } = usePoem();
    const poemLines = draftValues.poemLines ?? [];
    const rhymeScheme = draftValues.rhymeScheme ?? [];

    const unlockLine = (index: number) => {
        setUnlockedLines((prev) =>
            prev.includes(index) ? prev : [...prev, index]
        );
    };

    const updateLine = (index: number, newText: string) => {
        const updated = [...poemLines];
        updated[index] = newText;
        setDraftParam("poemLines", updated);
    };

    const clearLine = (index: number) => {
        updateLine(index, "");
    };

    useEffect(() => {
        if (poemLoading) {
            setUnlockedLines([]);
        }
    }, [poemLoading, poemError]);

    return (
        <div className="flex flex-row h-full pt-4">
            {
                (linesMode === "highlighted" || linesMode === "editable") && (
                    (poemLines && rhymeScheme) && (

                        <div className="w-[34px] py-6 leading-relaxed whitespace-pre-line font-[14px]">
                            <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                                {
                                    poemLines.map((line, i) => {
                                        switch (linesMode) {
                                            case "editable":
                                                return <PoemLinesEditBadge key={"edit-" + i} onClick={() => unlockLine(i)} locked={!unlockedLines.includes(i)} />;

                                            case "highlighted":
                                                const letter = (poemLines.length == rhymeScheme.length) ? rhymeScheme![i] : "?";
                                                const colorScheme = (poemLines.length == rhymeScheme.length) ? (SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings]) : "yellow";
                                                return <PoemLinesLetterBadge key={"letter-" + i} letter={letter} poemLineColorScheme={colorScheme} />;
                                        }
                                    })
                                }
                            </div>
                        </div>
                    )
                )
            }
            <Card className="flex flex-col h-full flex-1 mt-[-1px]">
                <CardContent className="pl-0 pr-6 py-6">
                    <div className="leading-relaxed whitespace-pre-line font-[14px]">
                        {
                            poemLoading && LoadingText()
                        }
                        {
                            poemError && ErrorText(poemError)
                        }
                        {
                            (!poemLoading && !poemError) &&
                                (poemLines && rhymeScheme) &&
                                    (
                                        <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                                            {
                                                poemLines.map((line, i) => {
                                                    switch (linesMode) {
                                                        case "editable":
                                                            return (
                                                                <PoemLine
                                                                    key={"edit-" + i}
                                                                    text={line}
                                                                    isEditable={true}
                                                                    locked={!unlockedLines.includes(i)}
                                                                    onChange={(newText) => updateLine(i, newText)}
                                                                    onClear={() => clearLine(i)} />
                                                            )

                                                        case "highlighted":
                                                            const letter = rhymeScheme![i];
                                                            const colorSchemeName = (poemLines.length == rhymeScheme.length) ? SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings] : "yellow";
                                                            const colorScheme = PoemLineColorSchemes[colorSchemeName];
                                                            return (
                                                                <PoemLine
                                                                    key={"letter-" + i}
                                                                    text={line}
                                                                    colorScheme={colorScheme} />
                                                            )

                                                        default:
                                                        case "plaintext":
                                                            return (
                                                                <PoemLine
                                                                    key={"plain-" + i}
                                                                    text={line} />
                                                            )
                                                    }
                                                })
                                            }
                                        </div>
                                    )
                        }
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}