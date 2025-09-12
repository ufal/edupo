import { create } from "zustand";
import { isEqual } from "lodash";
import defaultApiParams from "@/data/api/params-default-values.json";

type ParamValues = {
  id: string | null;
  author: string;
  title: string;
  poemLines: string[] | null;
  style: string;
  form: string;
  metre: string;
  rhyme: string;
  motives: string;
  rhymeScheme: string | null;
  temperature: number;
  syllablesCount: number;
  maxStrophes: number;
  versesCount: number;
};

type PoemParamsState = {
  currentValues: ParamValues;
  draftValues: ParamValues;
  initialValues: ParamValues;

  disabledFields: Record<keyof ParamValues, boolean>;
  initialDisabledFields: Record<keyof ParamValues, boolean>;

  poemLoading: boolean;
  poemError: string | null;

  alreadyLikedPoemIds: string[];
  addLikedPoemId: (id: string) => void;

  setPoemLoading: (loading: boolean) => void;
  setPoemError: (error: string | null) => void;

  setParam: <K extends keyof ParamValues>(key: K, value: ParamValues[K]) => void;
  setDraftParam: <K extends keyof ParamValues>(key: K, value: ParamValues[K]) => void;
  setDisabledField: (field: keyof ParamValues, value: boolean) => void;

  updateInitialValues: () => void;
  haveDraftParamsChanged: () => boolean;
  hasDraftParamChanged: (key: keyof ParamValues) => boolean;

  commitDraftToCurrent: () => void;
  resetDraft: () => void;
};

const defaultValues: ParamValues = {
  id: null,
  author: "",
  title: "",
  poemLines: null,
  style: "",
  form: "",
  metre: "",
  rhyme: "",
  motives: "",
  rhymeScheme: "",
  temperature: defaultApiParams.gen.temperature,
  syllablesCount: defaultApiParams.gen.syllablesCount,
  maxStrophes: defaultApiParams.gen.maxStrophes,
  versesCount: defaultApiParams.gen.versesCount,
};

const defaultDisabled: Record<keyof ParamValues, boolean> = {
  id: false,
  author: false,
  title: false,
  poemLines: false,
  style: false,
  form: false,
  metre: false,
  rhyme: false,
  motives: false,
  rhymeScheme: false,
  temperature: false,
  syllablesCount: false,
  maxStrophes: false,
  versesCount: false,
};

export const usePoem = create<PoemParamsState>((set, get) => ({
  currentValues: { ...defaultValues },
  draftValues: { ...defaultValues },
  initialValues: { ...defaultValues },

  disabledFields: { ...defaultDisabled },
  initialDisabledFields: { ...defaultDisabled },

  poemLoading: false,
  poemError: null,

  setPoemLoading: (loading: boolean) => set(() => ({ poemLoading: loading })),
  setPoemError: (error: string | null) => set(() => ({ poemError: error })),

  alreadyLikedPoemIds: [],

  addLikedPoemId: (id: string) =>
    set((state) => ({
      alreadyLikedPoemIds: [...state.alreadyLikedPoemIds, id]
    }
  )),

  setParam: (key, value) =>
    set((state) => ({
      currentValues: {
        ...state.currentValues,
        [key]: value,
      },
    })),

  setDraftParam: (key, value) =>
    set((state) => ({
      draftValues: {
        ...state.draftValues,
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
      draftValues: { ...state.currentValues },
    })),

  haveDraftParamsChanged: () => {
    const keys = Object.keys(defaultValues) as (keyof ParamValues)[];
    const { hasDraftParamChanged } = get();

    return keys.some((key) => hasDraftParamChanged(key));
  },

  hasDraftParamChanged: (key) => {
    const { currentValues, draftValues, initialDisabledFields, disabledFields } = get();

    const isDisabled = disabledFields[key];
    const wasDisabled = initialDisabledFields[key];

    const valueChanged = !isEqual(currentValues[key], draftValues[key]);
    const disabledChanged = wasDisabled !== isDisabled;

    if (isDisabled) {
      return disabledChanged;
    }

    return valueChanged || disabledChanged;
  },

  commitDraftToCurrent: () => {
    set((state) => ({
      currentValues: { ...state.draftValues },
    }))
  },

  resetDraft: () => {
    set((state) => ({
      draftValues: { ...state.currentValues },
    }))
  }
}));
