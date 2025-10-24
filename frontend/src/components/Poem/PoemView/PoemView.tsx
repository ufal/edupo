import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { PoemLinesLockedBadge, PoemLinesLetterBadge } from "./PoemLinesBadges";
import PoemLine from "./PoemLine/PoemLine";
import { SchemeToColorMappings } from "./SchemeToColorMappings";
import { PoemLineColorSchemes } from "./PoemLineColorSchemes";
import { usePoem } from "@/store/poemStore";
import PoemPlayBadge from "./PoemPlayBadge";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";

const ErrorText = (msg: string) => <p className="text-crimsonRed px-10">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft px-10">Načítám báseň...</p>;

type PoemViewLinesMode = "plaintext" | "highlighted" | "editable";

export default function PoemView({ linesMode } : { linesMode: PoemViewLinesMode }) {
    const [ unlockedLines, setUnlockedLines ] = useState<number[]>([]);

    const { draftValues, currentValues, setDraftParam, poemLoading, poemError } = usePoem();
    const { currentAnalysisValues } = usePoemAnalysis();

    const poemLines = draftValues.poemLines ?? [];
    const rhymeScheme = currentAnalysisValues.rhymeScheme ?? "";
    const isXRhymeScheme = rhymeScheme.split("").every(ch => ch === "X");
    //const isXRhymeScheme = Array(rhymeSchemeNormalized).every((val) => val === "X");

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

    const handleLineChange = (index: number, newText: string) => {
        const prevDraftLines = draftValues.poemLines ?? [];
        const currentLines   = currentValues.poemLines ?? [];

        const updatedDraftLines = [...prevDraftLines];
        updatedDraftLines[index] = newText;

        const newChangedIndexes: number[] = [];
        const lenAll = Math.max(updatedDraftLines.length, currentLines.length);
        for (let i = 0; i < lenAll; i++) {
            if (updatedDraftLines[i] !== currentLines[i]) {
                newChangedIndexes.push(i);
            }
        }

        setDraftParam("poemLines", updatedDraftLines);
        setDraftParam("changedPoemLineIndexes", newChangedIndexes);
    };

    useEffect(() => {
        if (poemLoading) {
            setUnlockedLines([]);
            setDraftParam("changedPoemLineIndexes", []);
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

    const lastChangedIndex = draftValues.changedPoemLineIndexes?.at(-1) ?? -1

    return (
        <div className="flex flex-row h-full pt-4 relative">
            {
                (linesMode === "highlighted" || linesMode === "editable") && (
                    (poemLines && rhymeScheme) && (

                        <div className="w-[40px] py-6 leading-tight whitespace-pre-line text-[16px]">
                            <div className="leading-tight whitespace-pre-line flex flex-col gap-1">
                                {
                                    poemLines.map((line, i) => {
                                        switch (linesMode) {
                                            case "editable":
                                                return <PoemLinesLockedBadge key={"edit-" + i} onClick={() => setLineLocking(false, i)} locked={!unlockedLines.includes(i)} />;

                                            case "highlighted":
                                                const letter = (poemLines.length == rhymeScheme.length) ? rhymeScheme![i] : "?";
                                                const colorSchemeName = (poemLines.length != rhymeScheme.length)
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
                                (poemLines && rhymeScheme) &&
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
                                                                    hasEditedBadge={draftValues.changedPoemLineIndexes?.includes(i)}
                                                                    locked={!unlockedLines.includes(i)}
                                                                    onChange={(newText) => handleLineChange(i, newText)}
                                                                    onBlur={() => setLineLocking(true, i)}
                                                                    onClear={() => clearLine(i)} />
                                                            )

                                                        case "highlighted":
                                                            const letter = isXRhymeScheme ? "X" : rhymeScheme![i];
                                                            const colorSchemeName = (poemLines.length != rhymeScheme.length)
                                                                                        ? "yellow"
                                                                                        : (typeof SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings] === "undefined")
                                                                                            ? "yellow"
                                                                                            : SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings]
                                                            const colorScheme = PoemLineColorSchemes[colorSchemeName];
                                                            
                                                            return (
                                                                <PoemLine
                                                                    key={"letter-" + i}
                                                                    text={line}
                                                                    hasLockedBadge={i <= lastChangedIndex}
                                                                    hasEditedBadge={draftValues.changedPoemLineIndexes?.includes(i)}
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