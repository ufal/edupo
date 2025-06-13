"use client"

import { useSearchParams } from "next/navigation";
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

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const poemId = params.get("poemId");
    setInitialPoemId(poemId);
  }, []);

  const [hasRunInitialLoad, setHasRunInitialLoad] = useState(false);

  const { loadPoem } = usePoemLoader();
  const { fetchAnalysis, fetchMotives } = usePoemGenerator();

  useEffect(() => {
    const run = async () => {
      if (hasRunInitialLoad) return;
      setHasRunInitialLoad(true);

      if (initialPoemId) {
          console.log("Loading initial poemId from URL:", initialPoemId);
          await loadPoem(initialPoemId);
          await usePoemDatabase.getState().fetchAuthors();
          return;
      }

      const newPoemId = await genPoem();
      if (!newPoemId) return;

      router.replace(`/?poemId=${newPoemId}`);
      await fetchAnalysis(newPoemId);
      await fetchMotives(newPoemId);
      await usePoemDatabase.getState().fetchAuthors();
    };

    run();
  }, [initialPoemId]);

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
