import PoemTitle from "./PoemTitle";
import PoemAnalysis from "./Modes/PoemAnalysis";
import PoemEditing from "./Modes/PoemEditing";
import PoeamReading from "./Modes/PoemReading/PoemReading";
import PoemModeSwitcher from "./PoemModeSwitcher";
import Footer from "@/components/layout/Footer";

import { PoemGenResult } from "@/types/poemGenResult";

interface PoemProps {
    poemGenResult: PoemGenResult;
    sidePanelControlElement: React.ReactNode
}

export default function Poem({ poemGenResult, sidePanelControlElement }: PoemProps) {
    return (
        <div className="w-full h-full flex flex-col">
            <PoemTitle
              authorName={poemGenResult.authorName}
              sidePanelControlElement={sidePanelControlElement} />
            <PoemModeSwitcher
              readingModeContent={<PoeamReading poemGenResult={poemGenResult} />}
              analysisModeContent={<PoemAnalysis poemGenResult={poemGenResult} />}
              editingModeContent={<PoemEditing poemGenResult={poemGenResult} />} />
            <Footer />
        </div>
    )
}