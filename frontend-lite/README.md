# EduPo Frontend Lite - "Namíchej si báseň"
Playful lightweight application built as an alternative frontend to EduPo poetry generation engine.

Applications invites the users to play with poem generation parameters via a visual metaphor of ingredients in a chemical reaction. Each ingredient represents one specific value of a poem generation parameter. These ingredients can be interactively dragged into a laboratory beaker and the reaction can be started. Starting the reaction calls EduPo API to generate a poem with the given parameters.

Ingredients are grouped by parameter (e.g. poem length) and only one ingredient (e.g. short poem or long poem) can be added to the beaker at the same time. Adding another ingredient of same type will exclude the previous ingredient of the same type from the beaker.

The app runs as a single-page application. It's written in TypeScript and bundled by Vite.

## Installation
Build application:
```bash
npm run build
```
Then copy contents of **./dist** directory to web hosting.

## Configuration
Settings are stored in [settings.json](./public/settings.json) and allow to configure the following properties externally, without editing source code:
- `api_url` URL of EduPo API, e.g. "https://quest.ms.mff.cuni.cz/edupo-api/"
- `share_url` URL for sharing the generated poem, e.g. "https://quest.ms.mff.cuni.cz/edupo-api/show?poemid={0}". Note the {0} placeholder for poem id.
- `api_default_params` Default API call parameters that don't change by user interaction, e.g. `modelspec` or `temperature`.
- `ingredients` Definition of available ingredients
    - `x`,`y` Position in ingredients container
    - `parameter` Name of the API parameter
    - `label` Text displayed in ingredient bubble
    - `value` Value of the API parameter
- `colors` HTML colors for every type of ingredient
- `target_points` Vacant positions for ingredients in the beaker
- `position_shuffle` Change to `true` if the ingredients should randomly change position on start
- `position_jitter_x`, `position_jitter_y` Randomly change initial position of ingredients by a small amount

All `x`, `y` coordinates use normalized values in the range [0,1] × [0,1] within their respective container.

Additional visual styling is possible in the [styles.css](./public/styles.css) file.
Both settings.json and styles.css are editable in **./dist** after build without the need for rebuilding the application.

## Requirements
The code has only few dependencies (TypeScript, Vite) and is built using a custom framework called [Fria (Framework for Real-time Interactive Applications)](./src/fria/). This framework is included directly in the codebase rather than as a dependency package because it has not been published yet.