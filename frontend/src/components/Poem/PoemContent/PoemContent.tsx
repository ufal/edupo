import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { PoemGenResult } from "@/types/poemGenResult";
import { PoemLinesEditBadge, PoemLinesLetterBadge } from "./PoemLinesBadge";
import PoemLine from "./PoemLine/PoemLine";
import { SchemeToColorMappings } from "./SchemeToColorMappings";
import { PoemLineColorSchemes } from "./PoemLineColorSchemes";

const ErrorText = (msg: string) => <p className="text-crimsonRed px-10">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft px-10">Načítám báseň...</p>;

type PoemContentLinesMode = "plaintext" | "highlighted" | "editable";

export default function PoemContent({ poemGenResult, linesMode } : { poemGenResult: PoemGenResult, linesMode: PoemContentLinesMode }) {
    const [unlockedLines, setUnlockedLines] = useState<number[]>([]);

    const unlockLine = (index: number) => {
        setUnlockedLines((prev) =>
            prev.includes(index) ? prev : [...prev, index]
        );
    };

    return (
        <div className="flex flex-row h-full">
            {
                (linesMode === "highlighted" || linesMode === "editable") && (
                    (poemGenResult.poemLines != null && poemGenResult.rhymeScheme != null && poemGenResult.poemLines?.length == poemGenResult.rhymeScheme?.length) && (

                        <div className="w-[34px] py-6 leading-relaxed whitespace-pre-line font-[14px]">
                            <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                                {
                                    poemGenResult.poemLines.map((line, i) => {
                                        switch (linesMode) {
                                            case "editable":
                                                return <PoemLinesEditBadge key={"edit-" + i} onClick={() => unlockLine(i)} locked={!unlockedLines.includes(i)} />;

                                            case "highlighted":
                                                const letter = poemGenResult.rhymeScheme![i];
                                                const colorScheme = SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings];
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
                            poemGenResult.loading && LoadingText()
                        }
                        {
                            poemGenResult.error && ErrorText(poemGenResult.error)
                        }
                        {
                            (poemGenResult.poemLines && poemGenResult.rhymeScheme && poemGenResult.poemLines.length == poemGenResult.rhymeScheme.length) && (
                                <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                                    {
                                        poemGenResult.poemLines.map((line, i) => {
                                            switch (linesMode) {
                                                case "editable":
                                                    return <PoemLine key={"edit-" + i} text={line} isEditable={true} locked={!unlockedLines.includes(i)} />;

                                                case "highlighted":
                                                    const letter = poemGenResult.rhymeScheme![i];
                                                    const colorSchemeName = SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings];
                                                    const colorScheme = PoemLineColorSchemes[colorSchemeName];
                                                    return <PoemLine key={"letter-" + i} text={line} colorScheme={colorScheme} />;

                                                default:
                                                case "plaintext":
                                                    return <PoemLine key={"plain-" + i} text={line} />;
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