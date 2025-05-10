import { PoemLineColorSchemeName } from "./PoemLineColorSchemes";

export type RhymeSchemeLetters = "A" | "B" | "C" | "X";

export const SchemeToColorMappings: Record<RhymeSchemeLetters, PoemLineColorSchemeName> = {
  "A": "pink",
  "B": "teal",
  "C": "sky",
  "X": "yellow"
};