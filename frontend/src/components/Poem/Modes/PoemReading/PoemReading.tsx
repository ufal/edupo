import { Card, CardContent } from "@/components/ui/card";
import { PoemGenResult } from "@/types/poemGenResult";

const ErrorText = (msg: string) => <p className="text-crimsonRed">Chyba: { msg }</p>;

const LoadingText = () => <p className="text-graySoft">Načítám báseň...</p>;

const PoemText = (lines: string[]) => (
    <div className="leading-relaxed whitespace-pre-line">
        { lines.map((line, i) => <div key={i} className="font-[14px]">{line}</div>) }
    </div>
);

interface PoemReadingProps {
    poemGenResult: PoemGenResult;
}

export default function PoemReading({ poemGenResult } : PoemReadingProps) {
    return (
        <Card className="flex flex-col h-full">
            <CardContent className="p-6">
                <div className="leading-relaxed whitespace-pre-line">
                    { poemGenResult.loading && LoadingText() }
                    { poemGenResult.error && ErrorText(poemGenResult.error) }
                    { poemGenResult.poemLines && PoemText(poemGenResult.poemLines) }
                </div>
            </CardContent>
        </Card>
    )
}