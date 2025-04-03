"use client"
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
    const [poemGenResult, setPoemGenResult] = useState<PoemGenResult>(initPoemGenResult);

    useEffect(() => {
        const fetchPoem = async () => {
          try {
            const url = process.env.NEXT_PUBLIC_API_URL! + "gen?metre=D&rhyme_scheme=ABABCC&syllables_count=12&verses_count=6&accept=json";
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