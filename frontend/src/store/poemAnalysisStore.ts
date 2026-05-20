import { create } from "zustand";

type AnalysisValues = {
  metre: "J" | "D" | "T" | "N" | null;
  metreAccuracy: number | null;
  metreConsistency: number | null;
  rhymeScheme: string | null;
  rhymeSchemeAccuracy: number | null;
  rhyming: number | null;
  rhymingConsistency: number | null;
  syllableCountEntropy: number | null;
  unknownWords: number | null;
};

const defaultValues: AnalysisValues = {
  metre: null,
  metreAccuracy: null,
  metreConsistency: null,
  rhymeScheme: null,
  rhymeSchemeAccuracy: null,
  rhyming: null,
  rhymingConsistency: null,
  syllableCountEntropy: null,
  unknownWords: null,
}

type AnalysisValuesState = {
  analysisLoading: boolean;
  setAnalysisLoading: (loading: boolean) => void;

  currentAnalysisValues: AnalysisValues;
  setAnalysisValue: <K extends keyof AnalysisValues>(key: K, value: AnalysisValues[K]) => void;
};

export const usePoemAnalysis = create<AnalysisValuesState>((set, get) => ({
  analysisLoading: false,

  setAnalysisLoading: (loading: boolean) => set(() => ({ analysisLoading: loading })),

  currentAnalysisValues: { ...defaultValues },

  setAnalysisValue: (key, value) =>
    set((state) => ({
      currentAnalysisValues: {
        ...state.currentAnalysisValues,
        [key]: value,
      },
    })),

}));