import { useRef, useCallback } from "react";

import { usePoem } from "@/store/poemStore";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";
import { genPoemApi, fetchPoemApi, fetchAnalysisApi, fetchMotivesApi, fetchImageApi, fetchTTSApi, sendLikeApi } from "@/lib/edupoApi";
import { MetreDetailCode, ImageResponse, TTSResponse, AnalysisResponse, FetchPoemResponse, GenResponse } from "@/types/edupoApi";

const GENERATED_FLAG = " [vygenerováno]";
const NO_TITLE_RESP = "Bez názvu";

const imageCache = new Map<string, { url: string; description: string }>();
const TTSCache = new Map<string, { url: string }>();

const parsePoemResponse = (data: FetchPoemResponse | GenResponse): { author: string; title: string; lines: string[]; rhymeScheme: string | null } => {
    const author = data.author_name ? data.author_name.replace(GENERATED_FLAG, "") : "";
    const title = data.title!;
    // const title =  (data.title === NO_TITLE_RESP) ? "" : data.title!;

    const plaintext = data.plaintext ?? "";
    const lines = plaintext.split("\n").filter(line => line.trim() !== "");

    let rhymeScheme = null;

    if (data.rawtext)
    {
        const schemeLine = data.rawtext.split("\n").find((line: string) => { return line.startsWith("#") && line.endsWith("#") }) ?? "";
        const parts = schemeLine.split("#");
        const schemeRaw = parts.length >= 2 ? parts[1] : "";
        rhymeScheme = schemeRaw.replace(/\s/g, "");
    }

    return { author, title, lines, rhymeScheme };
}

export function usePoemGenerator() {
    const { setAnalysisValue } = usePoemAnalysis();
    const { draftValues, currentValues, disabledFields, setDraftParam, commitDraftToCurrent, updateInitialValues, setPoemLoading, setPoemError } = usePoem.getState();

    const fetchPoem = useCallback(async (poemId: string): Promise<boolean> => {
        setPoemLoading(true);
        setPoemError(null);

        try {
            let params = new URLSearchParams({ accept: "json" });
            params.append("poemid", poemId.toString());

            const data = await fetchPoemApi(params);
            const parsedData = parsePoemResponse(data);

            console.log(parsedData);

            setDraftParam("title", data.title!);
            setDraftParam("author", parsedData.author);
            setDraftParam("poemLines", parsedData.lines);
            setDraftParam("rhymeScheme", parsedData.rhymeScheme);

            commitDraftToCurrent();

            setPoemLoading(false);
            return true;

        } catch (err: any) {
            console.error("Error fetching poem:", err);
            setPoemLoading(false);
            setPoemError(err.message || "Unknown error");
            return false;
        }
    }, [draftValues, disabledFields]);

    const genPoem = useCallback(async (): Promise<string | null> => {
        setPoemLoading(true);
        setPoemError(null);

        try {
            let params = new URLSearchParams({ accept: "json" });
            params.append("modelspec", "tm");

            if (!disabledFields.author && draftValues.author)
                params.append("author", draftValues.author);
            if (!disabledFields.title && draftValues.title)
                params.append("title", draftValues.title);
            if (!disabledFields.form)
                params.append("form", draftValues.form);
            if (!disabledFields.metre)
                params.append("metre", draftValues.metre);
            if (!disabledFields.rhymeScheme && draftValues.rhymeScheme)
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

            const data = await genPoemApi(params);
            const parsedData = parsePoemResponse(data);

            setDraftParam("id", data.id);
            setDraftParam("title", parsedData.title);
            setDraftParam("author", parsedData.author);
            setDraftParam("poemLines", parsedData.lines);
            setDraftParam("rhymeScheme", parsedData.rhymeScheme);

            commitDraftToCurrent();
            updateInitialValues();

            setPoemLoading(false);
            
            return data.id;

        } catch (err: any) {
            console.error("Error generating poem:", err);
            setPoemLoading(false);
            setPoemError(err.message || "Unknown error");
            return null;
        }
    }, [draftValues, disabledFields]);

    const fetchAnalysis = useCallback(async (id: string, onDataLoaded?: (analysisData: AnalysisResponse) => void) => {
        const data = await fetchAnalysisApi(id);

        if (onDataLoaded)
            onDataLoaded(data);

        const measures = data.measures;

        if (measures) {
            setAnalysisValue("metreAccuracy", measures.metre_accuracy);
            setAnalysisValue("metreConsistency", measures.metre_consistency);
            setAnalysisValue("rhymeSchemeAccuracy", measures.rhyme_scheme_accuracy);
            setAnalysisValue("rhyming", measures.rhyming);
            setAnalysisValue("rhymingConsistency", measures.rhyming_consistency);
            setAnalysisValue("syllableCountEntropy", measures.syllable_count_entropy);
            setAnalysisValue("unknownWords", measures.unknown_words);
        }

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
                setDraftParam("metre", firstCode);
        }

        commitDraftToCurrent(); // predpokladam/verim, ze alespon nejaky draftParam se nastavil
        updateInitialValues();

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

    const fetchImage = useCallback(async (poemId: string) => {
        if (imageCache.has(poemId))
            return imageCache.get(poemId)! as ImageResponse;

        const data = await fetchImageApi(poemId);
        const url = process.env.NEXT_PUBLIC_API_URL + (data.url?.slice(1) ?? "");
        const description = data.description ?? "";

        imageCache.set(poemId, { url, description });

        return { url, description } as ImageResponse;
    }, []);

    const fetchTTS = useCallback(async (poemId: string) => {
        if (TTSCache.has(poemId))
            return TTSCache.get(poemId)! as TTSResponse;

        const data = await fetchTTSApi(poemId);
        const url = process.env.NEXT_PUBLIC_API_URL + (data.url?.slice(1) ?? "");

        TTSCache.set(poemId, { url });
        return { url } as TTSResponse;
    }, []);

    const sendLike = useCallback(async (id: string) => {
        const data = await sendLikeApi(id);
        console.log("Like sent", data);
    }, []);

    return {
        fetchPoem,
        genPoem,
        fetchAnalysis,
        fetchMotives,
        fetchImage,
        fetchTTS,
        sendLike
    };
}