export type PoemLineColorSchemeName = "pink" | "teal" | "sky" | "yellow" | "violet" | "lime" | "crimson";

export type PoemLineColorScheme = {
  background: string;
  backgroundTransparent: string;
  foreground: string;
  text: string;
};

export const PoemLineColorSchemes: Record<PoemLineColorSchemeName, PoemLineColorScheme> = {
  pink: {
    background: 'pink200',
    backgroundTransparent: 'pink200Transparent',
    foreground: 'pink300',
    text: 'pink600',
  },
  teal: {
    background: 'teal200',
    backgroundTransparent: 'teal200Transparent',
    foreground: 'teal300',
    text: 'teal600',
  },
  sky: {
    background: 'sky200',
    backgroundTransparent: 'sky200Transparent',
    foreground: 'sky300',
    text: 'sky600',
  },
  yellow: {
    background: 'yellow200',
    backgroundTransparent: 'yellow200Transparent',
    foreground: 'yellow300',
    text: 'yellow600',
  },
  violet: {
    background: 'violet200',
    backgroundTransparent: 'violet200Transparent',
    foreground: 'violet300',
    text: 'violet600',
  },
  lime: {
    background: 'lime200',
    backgroundTransparent: 'lime200Transparent',
    foreground: 'lime300',
    text: 'lime600',
  },
  crimson: {
    background: 'crimson200',
    backgroundTransparent: 'crimson200Transparent',
    foreground: 'crimson300',
    text: 'crimson600',
  }
};
