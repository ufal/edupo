import PoemTitle from "./PoemTitle";

import PoemTabs from "./PoemTabs/PoemTabs";
import Footer from "@/components/layout/Footer";

interface PoemProps {
    sidePanelControlElement: React.ReactNode
}

export default function Poem({ sidePanelControlElement }: PoemProps) {
  return (
      <div className="w-full h-full flex flex-col">
          <PoemTitle sidePanelControlElement={sidePanelControlElement} />
          <PoemTabs />
          <Footer />
      </div>
  )
}