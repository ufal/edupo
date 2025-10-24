import { PoemLineColorSchemeName } from "./PoemLineColorSchemes";

export type RhymeSchemeLetters = "A" | "B" | "C" | "D" | "E" | "F" | "X";

export const SchemeToColorMappings: Record<RhymeSchemeLetters, PoemLineColorSchemeName> = {
  "A": "pink",
  "B": "teal",
  "C": "sky",
  "D": "lime",
  "E": "crimson",
  "F": "violet",
  "X": "yellow"
};