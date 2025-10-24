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
    red: HexColor;
    blue: HexColor;
  };
}

declare module "./frontends-config.json" {
  const value: AppConfig;
  export default value;
}
