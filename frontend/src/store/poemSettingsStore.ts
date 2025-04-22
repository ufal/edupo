import { create } from "zustand";
import isEqual from "lodash/isequal";
import defaultApiParams from "@/data/api/params-default-values.json";

type ParamValues = {
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
};

type PoemParamsState = {
  poemId: string | null;
  disabledFields: {
    author: boolean;
    name: boolean;
    style: boolean;
    form: boolean;
    metre: boolean;
    rhymeScheme: boolean;
    motives: boolean;
    versesCount: boolean;
    syllablesCount: boolean;
    temperature: boolean;
  };

  currentValues: ParamValues;
  initialValues: ParamValues;

  setPoemId: (value: string) => void;
  setParam: <K extends keyof ParamValues>(key: K, value: ParamValues[K]) => void;
  setDisabledField: (field: keyof PoemParamsState["disabledFields"], value: boolean) => void;

  updateInitialValues: () => void;
  haveParamsChanged: () => boolean;
  hasParamChanged: (key: keyof ParamValues) => boolean;
};

const defaultValues: ParamValues = {
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
};

export const usePoemParams = create<PoemParamsState>((set, get) => ({
  poemId: null,

  disabledFields: {
    author: false,
    name: false,
    style: false,
    form: false,
    metre: false,
    rhymeScheme: false,
    motives: false,
    versesCount: false,
    syllablesCount: false,
    temperature: false,
  },

  currentValues: { ...defaultValues },
  initialValues: { ...defaultValues },

  setPoemId: (value) => set({ poemId: value }),

  setParam: (key, value) =>
    set((state) => ({
      currentValues: {
        ...state.currentValues,
        [key]: value,
      },
    })),

  setDisabledField: (field, value) =>
    set((state) => ({
      disabledFields: {
        ...state.disabledFields,
        [field]: value,
      },
    })),

  updateInitialValues: () =>
    set((state) => ({
      initialValues: { ...state.currentValues },
    })),

  haveParamsChanged: () => {
    const { initialValues, currentValues } = get();
    return !isEqual(initialValues, currentValues);
  },

  hasParamChanged: (key) => {
    const { initialValues, currentValues } = get();
    return !isEqual(initialValues[key], currentValues[key]);
  },
}));
