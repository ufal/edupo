import PoemTitle from "./PoemTitle";
import PoemTabs from "./PoemTabs/PoemTabs";

interface PoemProps {
    sidePanelControlElement: React.ReactNode
}

export default function Poem({ sidePanelControlElement }: PoemProps) {
  return (
      <div className="w-full h-full flex flex-col">
          <PoemTitle sidePanelControlElement={sidePanelControlElement} />
          <PoemTabs />
      </div>
  )
}