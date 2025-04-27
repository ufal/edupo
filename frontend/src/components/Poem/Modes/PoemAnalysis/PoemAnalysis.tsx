import { Card, CardContent } from "@/components/ui/card";
import { PoemGenResult } from "@/types/poemGenResult";

interface PoemAnalysisProps {
    poemGenResult: PoemGenResult;
}

export default function PoemAnalysis({ poemGenResult } : PoemAnalysisProps) {
    return (
        <Card className="flex flex-col h-full">
            <CardContent>
                <p>
                    TODO
                </p>
            </CardContent>
        </Card>
    )
}