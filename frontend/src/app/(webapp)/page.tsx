"use client"

import { useState, useEffect } from "react";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { usePoemDatabase } from "@/store/poemDatabaseStore";

export default function Home() {

  const [openControlPanel, setOpenControlPanel] = useState(false);
  const { fetchPoem, fetchAnalysis, fetchMotives } = usePoemGenerator();

  useEffect(() => {
    usePoemDatabase.getState().fetchAuthors();
  }, []);

  useEffect(() => {
    const run = async () => {

      const newPoemId = await fetchPoem();
      await fetchAnalysis(newPoemId);
      await fetchMotives(newPoemId);
    };

    run();
  }, []);

  const sidePanelControlButton = (
    <SidePanelControlButton
      filled={openControlPanel}
      onClick={() => { setOpenControlPanel(!openControlPanel) }} />
  );

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">
        <Poem sidePanelControlElement={sidePanelControlButton} />
      </div>
      {
        openControlPanel && (
          <Sidebar>
            <PoemSettingsModeSwitcher />
          </Sidebar>
        )
      }
    </div>
  );
}
