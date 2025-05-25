import { create } from "zustand";
import isEqual from "lodash.isequal";
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
  currentValues: ParamValues;
  initialValues: ParamValues;

  disabledFields: Record<keyof ParamValues, boolean>;
  initialDisabledFields: Record<keyof ParamValues, boolean>;

  setParam: <K extends keyof ParamValues>(key: K, value: ParamValues[K]) => void;
  setDisabledField: (field: keyof ParamValues, value: boolean) => void;

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

const defaultDisabled: Record<keyof ParamValues, boolean> = {
  author: false,
  name: false,
  poemLines: false,
  style: false,
  form: false,
  metre: false,
  rhyme: false,
  motives: false,
  rhymeScheme: false,
  temperature: false,
  syllablesCount: false,
  versesCount: false,
};

export const usePoem = create<PoemParamsState>((set, get) => ({
  currentValues: { ...defaultValues },
  initialValues: { ...defaultValues },

  disabledFields: { ...defaultDisabled },
  initialDisabledFields: { ...defaultDisabled },

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
      initialDisabledFields: { ...state.disabledFields },
    })),

  haveParamsChanged: () => {
    const { initialValues, currentValues, initialDisabledFields, disabledFields } = get();
    return (
      !isEqual(initialValues, currentValues) ||
      !isEqual(initialDisabledFields, disabledFields)
    );
  },

  hasParamChanged: (key) => {
    const { initialValues, currentValues, initialDisabledFields, disabledFields } = get();
  
    const isDisabled = disabledFields[key];
    const wasDisabled = initialDisabledFields[key];
  
    const valueChanged = !isEqual(initialValues[key], currentValues[key]);
    const disabledChanged = wasDisabled !== isDisabled;
  
    if (isDisabled) {
      return disabledChanged;
    }
  
    return valueChanged || disabledChanged;
  }
}));
