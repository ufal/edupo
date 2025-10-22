import { create } from "zustand";

type AnalysisValues = {
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
  currentAnalysisValues: AnalysisValues;
  setAnalysisValue: <K extends keyof AnalysisValues>(key: K, value: AnalysisValues[K]) => void;
};

export const usePoemAnalysis = create<AnalysisValuesState>((set, get) => ({
  currentAnalysisValues: { ...defaultValues },

  setAnalysisValue: (key, value) =>
    set((state) => ({
      currentAnalysisValues: {
        ...state.currentAnalysisValues,
        [key]: value,
      },
    })),

}));