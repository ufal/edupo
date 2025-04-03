"use client"

import { useState } from "react";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import ImageSettings from "@/components/ImageSettings";
import PoemSettings from "@/components/PoemSettings";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

export default function Home() {
  const [openControlPanel, setOpenControlPanel] = useState(false);

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">
        <Poem sidePanelControlElement={
          <SidePanelControlButton
            filled={openControlPanel}
            onClick={() => { setOpenControlPanel(!openControlPanel) }} />
          } />
      </div>
      {
        openControlPanel && (
          <Sidebar>
            <PoemSettingsModeSwitcher poemModeContent={<PoemSettings />} imageModeContent={<ImageSettings />} />
          </Sidebar>
        )
      }
    </div>
  );
}
