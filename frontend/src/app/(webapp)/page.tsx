"use client"

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { usePoemDatabase } from "@/store/poemDatabaseStore";
import { usePoemLoader } from "@/hooks/useLoadPoem";

export default function Home() {

  const router = useRouter();

  const [openControlPanel, setOpenControlPanel] = useState(false);
  const { genPoem } = usePoemGenerator();
  
  const [initialPoemId, setInitialPoemId] = useState<string | null>(null);
  const [hasRunInitialLoad, setHasRunInitialLoad] = useState(false);
  const [hasTriedLoadingInitialPoem, setHasTriedLoadingInitialPoem] = useState(false);

  const { loadPoem } = usePoemLoader();
  const { fetchAnalysis, fetchMotives } = usePoemGenerator();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const poemId = params.get("poemId");
    setInitialPoemId(poemId);
  }, []);

  useEffect(() => {
    const run = async () => {
      if (hasRunInitialLoad) return;
      setHasRunInitialLoad(true);

      await usePoemDatabase.getState().fetchAuthors();

      const params = new URLSearchParams(window.location.search);
      const poemId = params.get("poemId");

      if (poemId) {
        console.log("Loading initial poemId from URL:", poemId);
        await loadPoem(poemId);
      } else {
        const newPoemId = await genPoem();
        if (!newPoemId) return;

        const currentPath = window.location.pathname;
        router.replace(`${currentPath}?poemId=${newPoemId}`);

        await fetchAnalysis(newPoemId);
        await fetchMotives(newPoemId);
      }
    };

    run();
  }, [hasRunInitialLoad]);

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
