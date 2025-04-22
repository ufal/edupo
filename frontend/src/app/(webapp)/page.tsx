"use client"

import { useState } from "react";
import { usePoemParams } from "@/store/poemSettingsStore";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import ImageSettings from "@/components/ImageSettings";
import PoemSettings from "@/components/PoemSettings";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

export default function Home() {
  const [poemKey, setPoemKey] = useState("");
  const [poemSettingsKey, setPoemSettingsKey] = useState("");
  const [openControlPanel, setOpenControlPanel] = useState(false);
  const { currentValues, disabledFields } = usePoemParams();

  const generateKey = () => {
    return [
      !disabledFields.metre ? currentValues.metre : undefined,
      !disabledFields.rhymeScheme ? currentValues.rhymeScheme : undefined,
      !disabledFields.temperature ? currentValues.temperature : undefined,
      !disabledFields.syllablesCount ? currentValues.syllablesCount : undefined,
      !disabledFields.versesCount ? currentValues.versesCount : undefined
    ].join("-");
  };

  const onAnalyseButtonClick = () => {
    setPoemSettingsKey(generateKey());
  };

  const onGenAnalyseButtonClick = () => {
    const rand = Math.random().toString(36).substring(2, 15);
    setPoemKey(rand);

    // TODO: zretezit to a analyzu spustit az po vygenerovani nove basne
    setTimeout(() => {
      setPoemSettingsKey(rand);
    }, 3000);
  };

  const sidePanelControlButton = (
    <SidePanelControlButton
      filled={openControlPanel}
      onClick={() => { setOpenControlPanel(!openControlPanel) }} />
  );

  const poemSettingsComponent = (
    <PoemSettings
      analyseButtonClick={onAnalyseButtonClick}
      genAnalyseButtonClick={onGenAnalyseButtonClick}
      key={poemSettingsKey} />
  );

  const imageSettingsComponent = <ImageSettings />;

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">
        <Poem
          sidePanelControlElement={sidePanelControlButton}
          key={poemKey} />
      </div>
      {
        openControlPanel && (
          <Sidebar>
            <PoemSettingsModeSwitcher
              poemModeContent={poemSettingsComponent}
              imageModeContent={imageSettingsComponent} />
          </Sidebar>
        )
      }
    </div>
  );
}
