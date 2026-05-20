import { AnalysisResponse } from "@/types/edupoApi";
import { usePoemGenerator } from "@/hooks/usePoemGenerator";

export function usePoemLoader() {
    const { fetchPoem, fetchAnalysis, fetchMotives } = usePoemGenerator();

    const loadPoem = async (poemId: string, fetchAnalysisCallback?: (data: AnalysisResponse) => void) => {
        const fetchSucc = await fetchPoem(poemId);

        if (fetchSucc)
        {
            await fetchAnalysis(poemId, fetchAnalysisCallback);
            await fetchMotives(poemId);
        }

    };

    return { loadPoem };
}