"use client"

import { useState } from "react";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import ImageSettings from "@/components/ImageSettings";
import PoemSettings from "@/components/PoemSettings";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

export default function Home() {
  const [poemKey, setPoemKey] = useState("");
  const [openControlPanel, setOpenControlPanel] = useState(false);

  const onAnalyseButtonClick = () => {
    setPoemKey(Date.now().toString());  // TODO - podle nastavených parametrů
  }

  const onGenAnalyseButtonClick = () => {
    setPoemKey(Date.now().toString());  // TODO - podle nastavených parametrů
  }

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">
        <Poem
          sidePanelControlElement={
            <SidePanelControlButton
              filled={openControlPanel}
              onClick={() => { setOpenControlPanel(!openControlPanel) }} />
          }
          key={poemKey} />
      </div>
      {
        openControlPanel && (
          <Sidebar>
            <PoemSettingsModeSwitcher poemModeContent={<PoemSettings analyseButtonClick={onAnalyseButtonClick} genAnalyseButtonClick={onGenAnalyseButtonClick} />} imageModeContent={<ImageSettings />} />
          </Sidebar>
        )
      }
    </div>
  );
}
