import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { PoemGenResult } from "@/types/poemGenResult";

import { usePoemParams } from "@/store/poemSettingsStore";

interface PoemEditingProps {
    poemGenResult: PoemGenResult;
}

export default function PoemEditing({ poemGenResult } : PoemEditingProps) {
    const setParam = usePoemParams((s) => s.setParam);

    return (
        <Card className="flex flex-col h-full">
            <CardContent>
                <p>
                    TODO
                </p>
                {
                    /*
                    <Button variant="outline" className="px-6 shadow-sm bg-white" onClick={() => { if (poemGenResult.poemLines) setParam("poemLines", poemGenResult.poemLines?.concat(["test 123"])) }}>
                        Změnit báseň
                    </Button>
                    */
                }
            </CardContent>
        </Card>
    )
}