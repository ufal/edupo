import { usePoem } from "@/store/poemStore";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";
import { fetchPoemApi, fetchAnalysisApi, fetchMotivesApi, sendLikeApi } from "@/lib/api/poemApi";
import { useCallback } from "react";
import { MetreDetailCode } from "@/types/edupoapi/analysis";

export function usePoemGenerator() {
    const { setAnalysisValue } = usePoemAnalysis();
    const { draftValues, currentValues, disabledFields, setDraftParam, commitDraftToCurrent, updateInitialValues, setPoemLoading, setPoemError } = usePoem.getState();

    const fetchPoem = useCallback(async (): Promise<string> => {
        setPoemLoading(true);
        setPoemError(null);

        try {
            let params = new URLSearchParams({ accept: "json" });

            if (!disabledFields.metre)
                params.append("metre", draftValues.metre);
            if (!disabledFields.rhymeScheme)
                params.append("rhyme_scheme", draftValues.rhymeScheme);
            if (!disabledFields.syllablesCount)
                params.append("syllables_count", draftValues.syllablesCount.toString());
            if (!disabledFields.versesCount)
                params.append("verses_count", draftValues.versesCount.toString());
            if (!disabledFields.temperature)
                params.append("temperature", draftValues.temperature.toString());

            const draftLines = draftValues.poemLines ?? [];
            const currentLines = currentValues.poemLines ?? [];
            const linesMaxLength = Math.max(draftLines.length, currentLines.length);

            const lastChangedIndex = Array.from({ length: linesMaxLength })
                .map((_, i) => i)
                .findLastIndex((i) => draftLines[i] !== currentLines[i]);

            const changedLines =
                lastChangedIndex >= 0
                ? draftLines.slice(0, lastChangedIndex + 1)
                : [];

            changedLines.forEach(line => {
                params.append("first_words", line);
            });

            const data = await fetchPoemApi(params);

            const plaintext = data.plaintext ?? "";
            const lines = plaintext.split("\n").filter(line => line.trim() !== "");

            const rawText = data.rawtext;
            const firstLine = rawText.split("\n")[0];
            const parts = firstLine.split("#");
            const scheme = parts.length >= 2 ? parts[1].trim() : "";

            setDraftParam("id", data.id);
            setDraftParam("name", data.title ?? "");
            setDraftParam("author", data.author_name ?? "");
            setDraftParam("poemLines", lines);
            setDraftParam("rhymeScheme", scheme);

            commitDraftToCurrent();
            updateInitialValues();

            setPoemLoading(false);
            
            return data.id;

        } catch (err: any) {
            console.error("Error fetching poem:", err);
            setPoemLoading(false);
            setPoemError(err.message || "Unknown error");
            return "";
        }
    }, [draftValues, disabledFields]);

    const fetchAnalysis = useCallback(async (id: string) => {
        const data = await fetchAnalysisApi(id);
        const measures = data.measures;
        setAnalysisValue("metreAccuracy", measures.metre_accuracy);
        setAnalysisValue("metreConsistency", measures.metre_consistency);
        setAnalysisValue("rhymeSchemeAccuracy", measures.rhyme_scheme_accuracy);
        setAnalysisValue("rhyming", measures.rhyming);
        setAnalysisValue("rhymingConsistency", measures.rhyming_consistency);
        setAnalysisValue("syllableCountEntropy", measures.syllable_count_entropy);
        setAnalysisValue("unknownWords", measures.unknown_words);

        const codes = data.body
            .map((item) => {
                const keys = Object.keys(item.metre) as MetreDetailCode[];
                return keys[0] ?? undefined;
            })
            .filter((code): code is MetreDetailCode => !!code);

        if (codes.length) {
            const firstCode = codes[0];
            const allSame = codes.every((code) => code === firstCode);

            if (allSame)
            {
                setDraftParam("metre", firstCode);
                commitDraftToCurrent();
                updateInitialValues();
            }
        }

    }, []);

    const fetchMotives = useCallback(async (id: string) => {
        const data = await fetchMotivesApi(id);
        if (Array.isArray(data.motives) && data.motives.length > 0) {
            const motives = data.motives
                .map(item => item.trim().replace(/^\d+\.\s*/, ""))
                .join(", ");
            setDraftParam("motives", motives);
            commitDraftToCurrent();
            updateInitialValues();
        }
    }, []);

    const sendLike = useCallback(async (id: string) => {
        const data = await sendLikeApi(id);
        console.log("Like sent", data);
    }, []);

    return {
        fetchPoem,
        fetchAnalysis,
        fetchMotives,
        sendLike
    };
}