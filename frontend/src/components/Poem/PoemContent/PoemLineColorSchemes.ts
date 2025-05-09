export type PoemLineColorSchemeName = "pink" | "teal" | "sky" | "yellow";

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
  }
};
