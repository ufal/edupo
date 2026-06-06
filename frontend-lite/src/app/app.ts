import type { Updatable } from "../fria/updatable";
import { UpdateDispatcher } from "../fria/update-dispatcher";
import { SerializablePoint, Settings } from "./settings";
import { Overlay } from "./classes/overlay";
import { Ingredient } from "./classes/ingredient";
import { Generator } from "./classes/generator";
import { EdupoAPI } from "./api/edupo-api";
import { IngredientManager } from "./classes/ingredient-manager";

import apphtml from "./html/app.html?raw";

import type { EdupoGenResponse } from "./api/edupo-gen-response";
import type { EdupoGenRequest } from "./api/edupo-api-request";
import type { IngredientSettings } from "./classes/ingredient-settings";


/**
 * The main class for the app, handles visual components and their logical classes.
 * HTML scaffold is loaded from apphtml import and injected into container element in index.html. 
 */

export class App implements Updatable
{
    /** The root container of the app */
    public element!:HTMLElement;

    /** Width of the container (used to detect resize events) */
    public width:number = 0;

    /** Height of the container (used to detect resize events) */
    public height:number = 0;
    
    private settings!:Settings;

    /** Creation and management of ingredients */
    public ingredientManager!:IngredientManager;
    
    public submitButton!:HTMLButtonElement;
    public resetButton!:HTMLButtonElement;

    /** Internal state of the application, 0 =  no ingredients in jar, 1 = ingredients in jar */
    private state:number = 0; /** TODO: REPLACE BY ENUM */

    private lastInteractionTime:number = Date.now();
    private readonly inactivityTimeoutMs:number = 60_000;

    /** Asynchronous connection to EduPo API  */
    public generator!:Generator;

    constructor(element:HTMLElement, params:any = {})
    {
        this.element = element;
        
        // Load settings
        fetch('settings.json')
        .then( (response:any) => response.json())
        .then( (data:any) => {
            this.settings = Settings.FromObject(data);
            this.settings.fill(params);
        })
        .catch( (response:any) => {
            console.error(`Settings not loaded: ${response}`);
            this.settings = Settings.FromObject(params);
        });
        
        // Check if both the container and settings are ready
        this.waitForInitialization();
    }

    public waitForInitialization()
    {
        // Make sure both setting and window are ready
        if (this.element.clientWidth == 0 || this.settings == undefined)
        {
            requestAnimationFrame( () => {this.waitForInitialization();});
        }
        else
        {
            // Start running the application
            UpdateDispatcher.Add(this);            
        }
    }

    public start()
    {        
        // Create HTML structures inside the container
        this.createHTML();

        // Create ingredients manager
        const drag_container = document.getElementById("epl_drag_container");
        const ingredients_container = document.getElementById("epl_ingredients_container");
        const jar_container = document.getElementById("epl_jar");
        const drop_zone = document.getElementById("epl_jar_dropzone");
        if (drag_container && ingredients_container && jar_container && drop_zone)
        {
            this.ingredientManager = new IngredientManager(drag_container, ingredients_container, jar_container, drop_zone);
        }

        // Create ingredients
        this.settings.ingredients.forEach( (bs:IngredientSettings) => {
            let b = this.ingredientManager.create(bs);
            if (b)
            {
                b.events.addEventListener("dragend", this.onDragEnd.bind(this));
                b.events.addEventListener("dragstart", this.onDragStart.bind(this));
                b.events.addEventListener("click", this.onIngredientClick.bind(this));
                UpdateDispatcher.Add(b);
            }
        });
        this.ingredientManager.calculateInitialPositions();

        // Create and initialize poem generator
        this.generator = new Generator(new EdupoAPI(Settings.Instance.api_url));

        // Reset inactivity timer on any pointer interaction
        this.element.addEventListener("pointerdown", () => { this.lastInteractionTime = Date.now(); });
        this.element.addEventListener("pointermove", () => { this.lastInteractionTime = Date.now(); });
    }

    public resize()
    {
        this.ingredientManager.resize();
    }   

    public update()
    {
        this.updateState();
        this.checkInactivity();
    }

    /** Creates necessary HTML elements inside app container, binds existing elements, attaches event handlers to DOM */
    private createHTML()
    {
        // Waiting modal overlay
        this.element.innerHTML = apphtml;    
        Overlay.Initialize(document.getElementById("epl_waiting_modal"));         
        UpdateDispatcher.Add(Overlay.Instance);

        // Target positions inside jar
        const jar = document.getElementById("epl_jar");
        if (jar)
        {
            for (let i = 0; i < Settings.Instance.target_points.length; i++)
            {
                let p:SerializablePoint = Settings.Instance.target_points[i];

                let div:HTMLDivElement = document.createElement("div");
                div.className = "epl_target_position";
                div.style.left = p.x * 100 + "%";
                div.style.top = p.y * 100 + "%";
                jar.appendChild(div);
            }
        }
       
        this.submitButton = document.getElementById("epl_btn_generate") as HTMLButtonElement;
        this.submitButton.style.visibility = "hidden";
        this.resetButton = document.getElementById("epl_btn_reset") as HTMLButtonElement;

        let cb = document.getElementById("epl_result_copy");
        cb?.addEventListener("click", async () => { this.copy();} );       
        
        // Disable dragging on img elements
        const imgs:HTMLElement[] = Array.from(document.getElementsByName("img"));
        imgs.forEach((img:HTMLElement) => { console.log(img.id); img.draggable = false});
        
    } 

    onDragStart(args:any[])
    {
        let b:Ingredient = args[0];
        this.ingredientManager.drag(b);
    }

    onDragEnd(args:any[])
    {
        let b:Ingredient = args[0];
        this.ingredientManager.drop(b);
    }

    onIngredientClick(args:any[])
    {
        let b:Ingredient = args[0];
        this.ingredientManager.click(b);
    }
    
    generate()
    {
        const call:EdupoAPI = new EdupoAPI(Settings.Instance.api_url);
        const request:EdupoGenRequest = this.ingredientManager.generateRequest();
        const startTime = Date.now();

        call.gen(request)
        .then(async (response:EdupoGenResponse) => {
                const elapsedMs = Date.now() - startTime;

                const res = document.getElementById("epl_result");
                const modal = document.getElementById("epl_result_modal");
                const buttons = document.getElementById("epl_result_buttons");
                // Hide Zavřít BEFORE making the modal visible so it never flashes
                // ahead of the poem (especially on the streaming path).
                if (buttons) buttons.style.visibility = "hidden";
                if (modal) modal.style.visibility = "visible";

                const share:HTMLAnchorElement = document.getElementById("epl_result_share") as any as HTMLAnchorElement;
                if (share)
                    {
                        share.href = Settings.Instance.share_url.replace('{0}', response.id);
                    }

                if (res)
                {
                    // Fast responses (typically cache hits) feel jarring when the whole
                    // poem appears at once -- reveal it word-by-word to give a sense
                    // that it's being "written".
                    if (elapsedMs < 5000)
                    {
                        await this.streamPoem(res, response.title, response.lines(), 150);
                    }
                    else
                    {
                        res.innerHTML = `<h2>${response.title}<br/></h2>${response.lines().join("<br/>")}`;
                    }
                }
                if (buttons) buttons.style.visibility = "visible";
            })
        .catch( (err:any) => {
            console.error(err)
        });
    }

    /**
     * Reveals a poem word by word into `container`, with `wordDelayMs` between words.
     * Uses textContent (not innerHTML) so the stream path doesn't render markup in
     * the title -- matches expected behaviour for plain-text poems.
     */
    async streamPoem(container:HTMLElement, title:string, lines:string[], wordDelayMs:number)
    {
        container.innerHTML = "";
        const sleep = (ms:number) => new Promise(r => setTimeout(r, ms));

        if (title)
        {
            const h2 = document.createElement("h2");
            container.appendChild(h2);
            const titleParts = title.split(/(\s+)/);
            for (const part of titleParts)
            {
                h2.appendChild(document.createTextNode(part));
                if (part.trim().length > 0) await sleep(wordDelayMs);
            }
            container.appendChild(document.createElement("br"));
        }

        for (let i = 0; i < lines.length; i++)
        {
            if (i > 0) container.appendChild(document.createElement("br"));
            const lineSpan = document.createElement("span");
            container.appendChild(lineSpan);
            const parts = lines[i].split(/(\s+)/);
            for (const part of parts)
            {
                lineSpan.appendChild(document.createTextNode(part));
                if (part.trim().length > 0) await sleep(wordDelayMs);
            }
        }
    }

    closeResult()
    {
        const modal = document.getElementById("epl_result_modal");
        if (modal)
        {
            modal.style.visibility = "hidden";
        }
        // Clear the inline visibility:visible set on the buttons row after streaming --
        // without this, it survives the parent modal going hidden (visibility doesn't
        // inherit across an explicit `visible` child) and Zavřít stays painted.
        const buttons = document.getElementById("epl_result_buttons");
        if (buttons) buttons.style.visibility = "";
    }

    public resetAll()
    {
        this.ingredientManager.returnAll();
        this.lastInteractionTime = Date.now();
    }

    private checkInactivity()
    {
        const modal = document.getElementById("epl_result_modal");
        const poemVisible = modal?.style.visibility === "visible";
        if (!poemVisible &&
            this.ingredientManager?.activeIngredients.length > 0 &&
            Date.now() - this.lastInteractionTime > this.inactivityTimeoutMs)
        {
            this.ingredientManager.returnAll();
            this.lastInteractionTime = Date.now();
        }
    }

    updateState()
    {
        let info1 = document.getElementById("epl_instruction_1");
        let info2 = document.getElementById("epl_instruction_2");

        if (info1 && info2)
        {
            if (this.state == 0)
            {
                if (this.ingredientManager.activeIngredients.length > 0)
                {
                    this.state = 1;
                    info1.style.display = "none";
                    info2.style.display = "block";
                    this.submitButton.style.visibility = "visible";
                    this.resetButton.style.visibility = "visible";
                }
            }
            else if (this.state == 1)
            {
                if (this.ingredientManager.activeIngredients.length < 1)
                {
                    this.state = 0;
                    info1.style.display = "block";
                    info2.style.display = "none";
                    this.submitButton.style.visibility = "hidden";
                    this.resetButton.style.visibility = "hidden";
                }
            }
        }
    }

    /**
     * Copies generated poem to clipboard
     */
    async copy()
    {
       const eplr:HTMLElement|null = document.getElementById("epl_result");
       if (eplr) 
       {
            const text = eplr.innerText;
            try {
                await navigator.clipboard.writeText(text);
            } 
            catch (err) {
                console.error("Failed to copy to clipboard:", err);
            }
       }
    }
}

/**
* Instantiates a new app inside the given element. 
* 
* @param elementId
* @param parameters
*/
export function init(elementId: string, parameters: any = {}):App|null
{
    let container = document.getElementById(elementId);
    if (container)
    {
        return new App(container, parameters);
    }
    else
    {
        console.error(`Element not found: ${elementId}`);
        return null;
    }
}