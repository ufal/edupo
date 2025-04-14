import { create } from "zustand";
import defaultApiParams from "@/data/default-api-params.json";

type PoemParamsState = {
  author: string;
  name: string;
  style: string;
  form: string;
  metre: string;
  rhyme: string;
  motives: string;
  rhymeScheme: string;
  temperature: number;
  syllablesCount: number;
  versesCount: number;
  disabledFields: {
    author: boolean;
    name: boolean;
    style: boolean;
    form: boolean;
    metrum: boolean;
    rhyme: boolean;
    motives: boolean;
    versesCount: boolean;
    syllablesCount: boolean;
    temperature: boolean;
  };
  setAuthor: (value: string) => void;
  setName: (value: string) => void;
  setStyle: (value: string) => void;
  setForm: (value: string) => void;
  setMetre: (value: string) => void;
  setRhyme: (value: string) => void;
  setMotives: (value: string) => void;
  setRhymeScheme: (value: string) => void;
  setTemperature: (value: number) => void;
  setSyllablesCount: (value: number) => void;
  setVersesCount: (value: number) => void;
  setDisabledField: (field: keyof PoemParamsState["disabledFields"], value: boolean) => void;
};

export const usePoemParams = create<PoemParamsState>((set) => ({
  author: "",
  name: "",
  style: "",
  form: "",
  metre: "",
  rhyme: "",
  motives: "",
  rhymeScheme: "",
  temperature: defaultApiParams.gen.temperature,
  syllablesCount: defaultApiParams.gen.syllablesCount,
  versesCount: defaultApiParams.gen.versesCount,
  disabledFields: {
    author: false,
    name: false,
    style: false,
    form: false,
    metrum: false,
    rhyme: false,
    motives: false,
    versesCount: false,
    syllablesCount: false,
    temperature: false,
  },
  setAuthor: (value) => set({ author: value }),
  setName: (value) => set({ name: value }),
  setStyle: (value) => set({ style: value }),
  setForm: (value) => set({ form: value }),
  setMetre: (value) => set({ metre: value }),
  setRhyme: (value) => set({ rhyme: value }),
  setMotives: (value) => set({ motives: value }),
  setRhymeScheme: (value) => set({ rhymeScheme: value }),
  setTemperature: (value) => set({ temperature: value }),
  setSyllablesCount: (value) => set({ syllablesCount: value }),
  setVersesCount: (value) => set({ versesCount: value }),
  setDisabledField: (field, value) =>
    set((state) => ({
      disabledFields: {
        ...state.disabledFields,
        [field]: value,
      },
    })),
}));
