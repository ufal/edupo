import { Card, CardContent } from "@/components/ui/card";
import { PoemGenResult } from "@/types/poemGenResult";
import PoemLinesBadges from "./PoemLinesBadges";
import PoemLine from "./PoemLine/PoemLine";
import { SchemeToColorMappings } from "./SchemeToColorMappings";
import { PoemLineColorSchemes } from "./PoemLineColorSchemes";

const ErrorText = (msg: string) => <p className="text-crimsonRed px-10">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft px-10">Načítám báseň...</p>;

type PoemContentLinesMode = "plaintext" | "highlighted" | "editable";

export default function PoemContent({ poemGenResult, linesMode } : { poemGenResult: PoemGenResult, linesMode: PoemContentLinesMode }) {
    return (
        <div className="flex flex-row h-full">
            {
                (linesMode === "highlighted") && <PoemLinesBadges poemGenResult={poemGenResult} type={"letter"} />
            }
            {
                (linesMode === "editable") && <PoemLinesBadges poemGenResult={poemGenResult} type={"editIcon"} />
            }
            <Card className="flex flex-col h-full flex-1 mt-[-1px]">
                <CardContent className="pl-0 pr-6 py-6">
                    <div className="leading-relaxed whitespace-pre-line font-[14px]">
                        { poemGenResult.loading && LoadingText() }
                        { poemGenResult.error && ErrorText(poemGenResult.error) }
                        {
                            (poemGenResult.poemLines && poemGenResult.rhymeScheme && poemGenResult.poemLines.length == poemGenResult.rhymeScheme.length) && (
                                <div className="leading-relaxed whitespace-pre-line flex flex-col gap-1">
                                    {
                                        poemGenResult.poemLines.map((line, i) => {
                                            switch (linesMode) {
                                                case "editable":
                                                    return <PoemLine key={i} text={line} isEditable={true} />;

                                                case "highlighted":
                                                    const letter = poemGenResult.rhymeScheme![i];
                                                    const colorSchemeName = SchemeToColorMappings[letter as keyof typeof SchemeToColorMappings];
                                                    const colorScheme = PoemLineColorSchemes[colorSchemeName];
                                                    return <PoemLine key={i} text={line} colorScheme={colorScheme} />;

                                                default:
                                                case "plaintext":
                                                    return <PoemLine key={i} text={line} />;
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