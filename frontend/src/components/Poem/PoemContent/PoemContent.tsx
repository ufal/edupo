import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { PoemLinesEditBadge, PoemLinesLetterBadge } from "./PoemLinesBadge";
import PoemLine from "./PoemLine/PoemLine";
import { SchemeToColorMappings } from "./SchemeToColorMappings";
import { PoemLineColorSchemes } from "./PoemLineColorSchemes";
import { usePoem } from "@/store/poemStore";
import PoemPlayBadge from "./PoemPlayBadge";

const ErrorText = (msg: string) => <p className="text-crimsonRed px-10">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft px-10">Načítám báseň...</p>;

type PoemContentLinesMode = "plaintext" | "highlighted" | "editable";

export default function PoemContent({ linesMode } : { linesMode: PoemContentLinesMode }) {
    const [unlockedLines, setUnlockedLines] = useState<number[]>([]);
    const { draftValues, currentValues, setDraftParam, poemLoading, poemError } = usePoem();
    const poemLines = draftValues.poemLines ?? [];
    const rhymeScheme = currentValues.rhymeScheme ?? "";
    let rhymeSchemeNormalized = rhymeScheme;

    if (rhymeSchemeNormalized.length != poemLines.length && poemLines.length % rhymeScheme.length === 0) {
        const repeatCount = poemLines.length / rhymeScheme.length;
        rhymeSchemeNormalized = rhymeScheme.repeat(repeatCount);
    }

    const isXRhymeScheme = Array(rhymeSchemeNormalized).every((val) => val === "X");

    const setLineLocking = (locked: boolean, index: number) => {
        if (locked) {
            setUnlockedLines((prev) => prev.filter((i) => i !== index));
        } else {
            setUnlockedLines((prev) => prev.includes(index) ? prev : [...prev, index]);
        }
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

    const heightElements = [
        { value: 64, unit: "px" },
        { value: 1, unit: "rem" },
        { value: 56, unit: "px" },
        { value: 1, unit: "rem" },
        { value: 40, unit: "px" },
        { value: 1, unit: "rem" },
        { value: 1.5, unit: "rem" },
        { value: 1.5, unit: "rem" },
        { value: 37, unit: "px" }
    ];

    const heightStr = `calc(100vh - ${heightElements
        .map((el) => `${el.value}${el.unit}`)
        .join(" - ")})`;

    return (
        <div className="flex flex-row h-full pt-4 relative">
            {
                (linesMode === "highlighted" || linesMode === "editable") && (
                    (poemLines && rhymeSchemeNormalized) && (

                        <div className="w-[40px] py-6 leading-tight whitespace-pre-line text-[16px]">
                            <div className="leading-tight whitespace-pre-line flex flex-col gap-1">
                                {
                                    poemLines.map((line, i) => {
                                        switch (linesMode) {
                                            case "editable":
                                                return <PoemLinesEditBadge key={"edit-" + i} onClick={() => setLineLocking(false, i)} locked={!unlockedLines.includes(i)} />;

                                            case "highlighted":
                                                const letter = (poemLines.length == rhymeSchemeNormalized.length) ? rhymeSchemeNormalized![i] : "?";
                                                const colorSchemeName = (poemLines.length != rhymeSchemeNormalized.length)
                                                                            ? "yellow"
                                                                            : (typeof SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings] === "undefined")
                                                                                ? "yellow"
                                                                                : SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings]
                                                return <PoemLinesLetterBadge key={"letter-" + i} letter={letter} poemLineColorScheme={colorSchemeName} />;
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
                    <div className="leading-tight whitespace-pre-line text-[16px] overflow-auto" style={{ maxHeight: heightStr}}>
                        {
                            poemLoading && LoadingText()
                        }
                        {
                            poemError && ErrorText(poemError)
                        }
                        {
                            (!poemLoading && !poemError) &&
                                (poemLines && rhymeSchemeNormalized) &&
                                    (
                                        <div className="leading-tight whitespace-pre-line flex flex-col gap-1">
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
                                                                    onBlur={() => setLineLocking(true, i)}
                                                                    onClear={() => clearLine(i)} />
                                                            )

                                                        case "highlighted":
                                                            const letter = isXRhymeScheme ? "X" : rhymeSchemeNormalized![i];
                                                            const colorSchemeName = (poemLines.length != rhymeSchemeNormalized.length)
                                                                                        ? "yellow"
                                                                                        : (typeof SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings] === "undefined")
                                                                                            ? "yellow"
                                                                                            : SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings]
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
            <PoemPlayBadge cls="absolute left-4 bottom-4" />
        </div>
    )
}