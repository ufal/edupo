type HexColor = `#${string}`;
type AppPath = `/${string}`;

export interface AppConfig {
  FRONTEND: {
    URL: {
      poemRead: AppPath;
      poemAnalyze: AppPath;
      poemEdit: AppPath;
      poemVisualize: AppPath;
    };
  };
  palette: {
    colorGrey50: HexColor;
    colorGrey100: HexColor;
    colorGrey200: HexColor;
    colorGrey300: HexColor;
    colorGrey400: HexColor;
    colorGrey500: HexColor;
    colorGrey600: HexColor;
    colorGrey700: HexColor;
    colorGrey800: HexColor;
    colorGrey900: HexColor;

    colorPurple50: HexColor;
    colorPurple100: HexColor;
    colorPurple200: HexColor;
    colorPurple300: HexColor;
    colorPurple400: HexColor;
    colorPurple500: HexColor;
    colorPurple600: HexColor;
    colorPurple700: HexColor;
    colorPurple800: HexColor;
    colorPurple900: HexColor;

    colorYellow50: HexColor;
    colorYellow100: HexColor;
    colorYellow200: HexColor;
    colorYellow300: HexColor;
    colorYellow400: HexColor;
    colorYellow500: HexColor;
    colorYellow600: HexColor;
    colorYellow700: HexColor;
    colorYellow800: HexColor;
    colorYellow900: HexColor;

    colorCyan50: HexColor;
    colorCyan100: HexColor;
    colorCyan200: HexColor;
    colorCyan300: HexColor;
    colorCyan400: HexColor;
    colorCyan500: HexColor;
    colorCyan600: HexColor;
    colorCyan700: HexColor;
    colorCyan800: HexColor;
    colorCyan900: HexColor;

    colorTeal50: HexColor;
    colorTeal100: HexColor;
    colorTeal200: HexColor;
    colorTeal300: HexColor;
    colorTeal400: HexColor;
    colorTeal500: HexColor;
    colorTeal600: HexColor;
    colorTeal700: HexColor;
    colorTeal800: HexColor;
    colorTeal900: HexColor;
  };
}

declare module "./frontends-config.json" {
  const value: AppConfig;
  export default value;
}
