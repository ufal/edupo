import PoemTitle from "./PoemTitle";
import PoemContent from "./PoemContent/PoemContent";
import PoemModeSwitcher from "./PoemModeSwitcher";
import Footer from "@/components/layout/Footer";

import { usePoem } from "@/store/poemStore";
import { PoemGenResult } from "@/types/poemGenResult";

interface PoemProps {
    poemGenResult: PoemGenResult;
    sidePanelControlElement: React.ReactNode
}

export default function Poem({ poemGenResult, sidePanelControlElement }: PoemProps) {
  const { currentValues } = usePoem();

  return (
      <div className="w-full h-full flex flex-col">
          <PoemTitle
            authorName={currentValues.author}
            sidePanelControlElement={sidePanelControlElement} />
          <PoemModeSwitcher
            readingModeContent={<PoemContent poemGenResult={poemGenResult} linesMode="plaintext" />}
            analysisModeContent={<PoemContent poemGenResult={poemGenResult} linesMode="highlighted" />}
            editingModeContent={<PoemContent poemGenResult={poemGenResult} linesMode="editable" />} />
          <Footer />
      </div>
  )
}