"use client"

import { usePoemParams } from "@/store/poemSettingsStore";
import { useState, useEffect } from "react";

import PoemTitle from "./PoemTitle";
import PoemAnalysis from "./Modes/PoemAnalysis";
import PoemEditing from "./Modes/PoemEditing";
import PoeamReading from "./Modes/PoemReading/PoemReading";
import PoemModeSwitcher from "./PoemModeSwitcher";
import Footer from "@/components/layout/Footer";
import { GenResponse } from "@/types/edupoapi/gen";

interface PoemProps {
    sidePanelControlElement: React.ReactNode
}

export interface PoemGenResult {
    loading: boolean;
    error: string | null;
    authorName: string | null;
    poemLines: string[] | null;
}

const initPoemGenResult: PoemGenResult = {
    loading: true,
    error: null,
    authorName: null,
    poemLines: null
}

export default function Poem({ sidePanelControlElement }: PoemProps) {
    const { metre, rhymeScheme, temperature, syllablesCount, versesCount, disabledFields } = usePoemParams();
    const [poemGenResult, setPoemGenResult] = useState<PoemGenResult>(initPoemGenResult);

    useEffect(() => {
        const fetchPoem = async () => {
          try {

            const baseUrl = process.env.NEXT_PUBLIC_API_URL!;
            const endpoint = "gen";
            
            const params = new URLSearchParams({
              metre,
              rhyme_scheme: rhymeScheme,
              syllables_count: syllablesCount.toString(),
              verses_count: versesCount.toString(),
              accept: "json",
            });
            
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

            const plaintext = data.plaintext;
    
            if (typeof plaintext !== "string" || plaintext.trim() === "") {
              throw new Error("Missing or invalid 'plaintext' in response");
            }
    
            const lines = plaintext.split("\n").filter(line => line.trim() !== "");
    
            if (lines.length < 1) {
              throw new Error("Poem appears to be empty");
            }
    
            setPoemGenResult({
                loading: false,
                error: null,
                authorName: data.author_name || null,
                poemLines: lines
            });

          } catch (err: any) {

            console.error("Error fetching poem:", err);
            setPoemGenResult({
                loading: false,
                error: err.message || "Unknown error",
                authorName: null,
                poemLines: null
            });
          }
        };
    
        fetchPoem();
    }, []);

    return (
        <div className="w-full h-full flex flex-col">
            <PoemTitle poemGenResult={poemGenResult} sidePanelControlElement={sidePanelControlElement} />
            <PoemModeSwitcher readingModeContent={<PoeamReading poemGenResult={poemGenResult} />} analysisModeContent={<PoemAnalysis />} editingModeContent={<PoemEditing />} />
            <Footer />
        </div>
    )
}