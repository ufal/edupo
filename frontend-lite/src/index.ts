import config from "../../frontends-config.json";

const examplePoemId = 123;
const poemUrl = config.FRONTEND.URL.poemAnalysis.replace("{0}", String(examplePoemId));

console.log("URL básně:", poemUrl);
console.log("Primární barva:", config.palette.colorPurple500);