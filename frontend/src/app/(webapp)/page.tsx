"use client"

import { usePoemParams } from "@/store/poemSettingsStore";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";
import { useState, useEffect, useCallback } from "react";

import { GenResponse } from "@/types/edupoapi/gen";
import { AnalysisResponse } from "@/types/edupoapi/analysis";
import { PoemGenResult } from "@/types/poemGenResult";

import Poem from "@/components/Poem";
import Sidebar from "@/components/layout/Sidebar";
import ImageSettings from "@/components/ImageSettings";
import PoemSettings from "@/components/PoemSettings";
import SidePanelControlButton from "@/components/SidePanelControlButton";
import PoemSettingsModeSwitcher from "@/components/PoemSettings/PoemSettingsModeSwitcher";

const initPoemGenResult: PoemGenResult = {
  loading: true,
  error: null,
  authorName: null,
  poemLines: null
}

export default function Home() {
  const [poemId, setPoemId] = useState(null);
  const [openControlPanel, setOpenControlPanel] = useState(false);
  const [poemGenResult, setPoemGenResult] = useState<PoemGenResult>(initPoemGenResult);
  const { updateInitialValues } = usePoemParams();
  const { setAnalysisValue } = usePoemAnalysis();

  const setParam = usePoemParams((s) => s.setParam);
  const fetchAnalysis = useCallback(async (overrideId = null) => {

    const idToUse = overrideId ?? poemId;
    const { currentValues, disabledFields } = usePoemParams.getState();

    if (!idToUse) return;

    try {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL!;
        const endpoint = "analyze";
        
        let params = new URLSearchParams({
            accept: "json"
        });
  
        if (!disabledFields.versesCount)
            params.append("poemid", idToUse!);
  
        const res = await fetch(`${baseUrl}${endpoint}?${params}`);

        let data: AnalysisResponse;

        try {
          data = await res.json();
        } catch (jsonErr) {
          throw new Error("Failed to parse JSON response");
        }
  
        if (!data || typeof data !== "object") {
          throw new Error("Unexpected response format");
        }

        if (!data.measures || typeof data.measures !== "object") {
          throw new Error("Missing or invalid 'measures' in response");
        }

        const measures = data.measures;
        setAnalysisValue("metreAccuracy", measures.metre_accuracy);
        setAnalysisValue("metreConsistency", measures.metre_consistency);
        setAnalysisValue("rhymeSchemeAccuracy", measures.rhyme_scheme_accuracy);
        setAnalysisValue("rhyming", measures.rhyming);
        setAnalysisValue("rhymingConsistency", measures.rhyming_consistency);
        setAnalysisValue("syllableCountEntropy", measures.syllable_count_entropy);
        setAnalysisValue("unknownWords", measures.unknown_words);

    } catch (error) {
        console.error("Error fetching analysis:", error);
    }

    console.log(`Fetching analysis for poem ${idToUse}...`);
    
  }, [poemId]);

  const fetchPoem = useCallback(async () => {

    const { currentValues, disabledFields } = usePoemParams.getState();

    setPoemGenResult({
      loading: true,
      error: poemGenResult.error,
      authorName: poemGenResult.authorName,
      poemLines: poemGenResult.poemLines
    });

    try {
      console.log("Fetching poem...", poemId);

      const baseUrl = process.env.NEXT_PUBLIC_API_URL!;
      const endpoint = "gen";
      
      let params = new URLSearchParams({
        accept: "json"
      });
      
      if (!disabledFields.metre)
        params.append("metre", currentValues.metre);

      if (!disabledFields.rhymeScheme)
        params.append("rhyme_scheme", currentValues.rhymeScheme);

      if (!disabledFields.syllablesCount)
        params.append("syllables_count", currentValues.syllablesCount.toString());

      if (!disabledFields.versesCount)
        params.append("verses_count", currentValues.versesCount.toString());

      if (!disabledFields.temperature)
        params.append("temperature", currentValues.temperature.toString());
      
      const url = `${baseUrl}${endpoint}?${params.toString()}`;
      const res = await fetch(url);

      if (!res.ok) {
        throw new Error(`Server returned ${res.status} ${res.statusText}`);
      }

      let data: GenResponse;

      try {
        data = await res.json();
      } catch (jsonErr) {
        throw new Error("Failed to parse JSON response");
      }

      if (!data || typeof data !== "object") {
        throw new Error("Unexpected response format");
      }

      /*
      const data =
        {
          "author_name": "Anonym [vygenerov\u00e1no]",
          "geninput": {
              "anaphors": [],
              "author_name": "Anonym",
              "epanastrophes": [],
              "first_words": [],
              "max_strophes": 2,
              "metre": "D",
              "modelspec": "mc",
              "rhyme_scheme": "ABABCC",
              "syllables_count": 12,
              "temperature": 1.0,
              "title": "Bez n\u00e1zvu",
              "verses_count": 6
          },
          "id": "2025-04-13_21-29-47_igkqKOyQcOo",
          "plaintext": "A v tom, jak v poh\u00e1dce, v tom \u010darovn\u00e9m usm\u00e1n\u00ed\nv tom, jak se v poh\u00e1dku v\u0161ecko se m\u011bn\u00ed,\nv tom, jak se v poh\u00e1dce v\u0161ecko se ukl\u00e1n\u00ed,\nv tom, jak se v poh\u00e1dce v\u0161ecko to cen\u00ed,\nv tom, jak se v poh\u00e1dce v\u0161ecko to pozn\u00e1n\u00ed,\nv tom, jak se v poh\u00e1dce v\u0161ecko to pozn\u00e1n\u00ed.",
          "rawtext": "# ABABCC # 1900\nD # 12 # \u00e1n\u00ed # a v tom, jak v poh\u00e1dce, v tom \u010darovn\u00e9m usm\u00e1n\u00ed\nD # 11 # \u011bn\u00ed # v tom, jak se v poh\u00e1dku v\u0161ecko se m\u011bn\u00ed,\nD # 12 # \u00e1n\u00ed # v tom, jak se v poh\u00e1dce v\u0161ecko se ukl\u00e1n\u00ed,\nD # 11 # en\u00ed # v tom, jak se v poh\u00e1dce v\u0161ecko to cen\u00ed,\nD # 12 # \u00e1n\u00ed # v tom, jak se v poh\u00e1dce v\u0161ecko to pozn\u00e1n\u00ed,\nD # 12 # \u00e1n\u00ed # v tom, jak se v poh\u00e1dce v\u0161ecko to pozn\u00e1n\u00ed,\n<|endoftext|>",
          "title": "Bez n\u00e1zvu"
      };
      */

      console.log(data);
      
      const plaintext = data.plaintext;

      if (typeof plaintext !== "string" || plaintext.trim() === "") {
        throw new Error("Missing or invalid 'plaintext' in response");
      }

      const lines = plaintext.split("\n").filter(line => line.trim() !== "");

      if (lines.length < 1) {
        throw new Error("Poem appears to be empty");
      }

      setPoemId(data.id);
      
      setParam("poemLines", lines);
      updateInitialValues();

      setPoemGenResult({
          loading: false,
          error: null,
          authorName: data.author_name || null,
          poemLines: lines
      });

      fetchAnalysis(data.id);
    } catch (err: any) {

      console.error("Error fetching poem:", err);
      setPoemGenResult({
          loading: false,
          error: err.message || "Unknown error",
          authorName: null,
          poemLines: null
      });
    }

  }, []);

  useEffect(() => {
    fetchPoem();
  }, [fetchPoem]);

  const onAnalyseButtonClick = () => {
    fetchAnalysis();
  };

  const onGenAnalyseButtonClick = () => {
    fetchPoem();
  };

  const sidePanelControlButton = (
    <SidePanelControlButton
      filled={openControlPanel}
      onClick={() => { setOpenControlPanel(!openControlPanel) }} />
  );

  const poemSettingsComponent = (
    <PoemSettings
      analyseButtonClick={onAnalyseButtonClick}
      genAnalyseButtonClick={onGenAnalyseButtonClick} />
  );

  const imageSettingsComponent = <ImageSettings />;

  return (
    <div className="flex h-full">
      <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pt-4">
        <Poem
          poemGenResult={poemGenResult}
          sidePanelControlElement={sidePanelControlButton} />
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
