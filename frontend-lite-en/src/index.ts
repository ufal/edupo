import config from "../../frontends-config.json";

const examplePoemId = 123;
const poemUrl = config.FRONTEND.URL.poemAnalysis.replace("{0}", String(examplePoemId));

console.log("Poem URL:", poemUrl);
console.log("Primary color:", config.palette.colorPurple500);
