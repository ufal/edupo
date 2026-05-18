import PoemTitle from "./PoemTitle";
import PoemTabs from "./PoemTabs/PoemTabs";
import { PoemViewMode } from "@/components/Poem/PoemView/PoemView";

export default function Poem({ defaultMode, sidePanelControlElement }: { sidePanelControlElement: React.ReactNode; defaultMode?: PoemViewMode;}) {
  return (
      <div className="w-full h-full flex flex-col">
          <PoemTitle sidePanelControlElement={sidePanelControlElement} />
          <PoemTabs defaultMode={ defaultMode} />
      </div>
  )
}