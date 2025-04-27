import { create } from "zustand";
import isEqual from "lodash/isequal";
import defaultApiParams from "@/data/api/params-default-values.json";

type ParamValues = {
  author: string;
  name: string;
  poemLines: string[] | null;
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

  disabledFields: {
    author: boolean;
    name: boolean;
    poemLines: boolean;
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

  setParam: <K extends keyof ParamValues>(key: K, value: ParamValues[K]) => void;
  setDisabledField: (field: keyof PoemParamsState["disabledFields"], value: boolean) => void;

  updateInitialValues: () => void;
  haveParamsChanged: () => boolean;
  hasParamChanged: (key: keyof ParamValues) => boolean;
};

const defaultValues: ParamValues = {
  author: "",
  name: "",
  poemLines: null,
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

  disabledFields: {
    author: false,
    name: false,
    poemLines: false,
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
