"use client"

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemControls/PoemSettingsModeSwitcher";

import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { usePoemDatabase } from "@/store/poemDatabaseStore";
import { usePoemLoader } from "@/hooks/useLoadPoem";

import { PoemViewMode } from "@/components/Poem/PoemView/PoemView";
import { PoemSettingsMode } from "@/components/PoemControls/PoemSettingsModeSwitcher/PoemSettingsModeSwitcher";

export default function Home() {
  const router = useRouter();

  const [openControlPanel, setOpenControlPanel] = useState(false);

  const [defaultViewMode, setDefaultViewMode] = useState<PoemViewMode | null>(null);
  const [defaultSettingsMode, setDefaultSettingsMode] = useState<PoemSettingsMode | null>(null);

  const [hasModesReady, setHasModesReady] = useState(false);
  const [poemReady, setPoemReady] = useState(false);

  const { genPoem, fetchAnalysis, fetchMotives } = usePoemGenerator();
  const { loadPoem } = usePoemLoader();

  const [hasRunInitialLoad, setHasRunInitialLoad] = useState(false);

  useEffect(() => {
    const run = async () => {
      if (hasRunInitialLoad) return;
      setHasRunInitialLoad(true);

      usePoemDatabase.getState().fetchAuthors().catch(() => {});
      const params = new URLSearchParams(window.location.search);

      const viewModeParam = params.get("viewMode");
      if (
        viewModeParam === "reading" ||
        viewModeParam === "analysis" ||
        viewModeParam === "editing"
      ) {
        setDefaultViewMode(viewModeParam as PoemViewMode);
      } else {
        setDefaultViewMode("reading");
      }

      const controlsParam = params.get("controls");
      if (controlsParam === "poem" || controlsParam === "image") {
        setDefaultSettingsMode(controlsParam as PoemSettingsMode);
        setOpenControlPanel(true);
      } else {
        setDefaultSettingsMode("poem");
        setOpenControlPanel(false);
      }

      setHasModesReady(true);

      const poemIdFromUrl = params.get("poemId");
      let activePoemId = poemIdFromUrl;

      if (poemIdFromUrl) {
        await loadPoem(poemIdFromUrl);
      } else {
        const newPoemId = await genPoem();
        if (!newPoemId) {
          setPoemReady(true);
          return;
        }

        activePoemId = newPoemId;

        params.set("poemId", newPoemId);
        const currentPath = window.location.pathname;
        router.replace(`${currentPath}?${params.toString()}`);

        await loadPoem(newPoemId);

        fetchAnalysis(newPoemId).catch(() => {});
        fetchMotives(newPoemId).catch(() => {});
      }

      setPoemReady(true);
    };

    run();
  }, [
    hasRunInitialLoad,
    router,
    genPoem,
    loadPoem,
    fetchAnalysis,
    fetchMotives,
  ]);

  // tlačítko pro sidebar (to klidně můžeme ukázat hned jak známe módy)
  const sidePanelControlButton = hasModesReady ? (
    <SidePanelControlButton
      filled={openControlPanel}
      onClick={() => {
        setOpenControlPanel(!openControlPanel);
      }}
    />
  ) : null;

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">

        {!hasModesReady && (
          <div className="text-muted-foreground text-sm">Loading…</div>
        )}

        {/*
          hasModesReady && !poemReady && (
          <div className="space-y-2">
            {sidePanelControlButton}
            <div className="text-muted-foreground text-sm">Loading poem…</div>
          </div>
          )
        */}

        {hasModesReady && (
          <Poem
            defaultMode={defaultViewMode as PoemViewMode}
            sidePanelControlElement={sidePanelControlButton}
          />
        )}
      </div>

      {hasModesReady && openControlPanel && (
        <Sidebar>
          <PoemSettingsModeSwitcher
            defaultMode={defaultSettingsMode as PoemSettingsMode}
          />
        </Sidebar>
      )}
    </div>
  );
}