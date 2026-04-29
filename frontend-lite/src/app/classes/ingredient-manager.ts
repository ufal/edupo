import { EdupoGenRequest } from "../api/edupo-api-request";
import { TextBubble } from "../bubbles/text-bubble";
import { Ingredient } from "./ingredient";
import { IngredientSettings } from "./ingredient-settings";

import text_bubble_html from "../bubbles/text-bubble.html?raw";
import { dist, randomInt } from "../../fria/helpers";
import { Point, Rectangle } from "../../fria/geometry";
import { Settings } from "../settings";
import { JarTargetPosition } from "./jar-target-position";
import { VisualElement } from "../../fria/visual-element";

/**
 * Manages ingredients from their creation, through their dragging and dropping, 
 * up to generating a request based on the ingredients in the jar. 
 */
export class IngredientManager
{
    /**
     * All ingredients in the application
     */
    public ingredients:Ingredient[] = [];

    /**
     * Container used for initial positions of the ingredients. 
     */
    public sourceContainer!:HTMLElement;
    
    /**
     * Container for dragging the ingredients around. This is 
     */
    public dragContainer!:HTMLElement;    

    /**
     * Container where the active ingredients are placed and animated
     */
    public targetContainer!:HTMLElement;

    /**
     * Area for dropping the ingredients. Drop zone doesn't have to be the same shape or size as targetContainer
     */
    public dropZone!:HTMLElement;

    /**
     * Set of ingredients which are 'active', i.e. they are in the jar and will be used in forming API request.
     */
    public activeIngredients:Ingredient[] = [];

    /**
     * Positions in the jar to which ingredients are snapped when dropped to jar.
     */
    public targetPositions:JarTargetPosition[] = [];

    constructor(dragContainer:HTMLElement, sourceContainer:HTMLElement, targetContainer:HTMLElement, dropZone:HTMLElement)
    {
        this.dragContainer = dragContainer;
        this.sourceContainer = sourceContainer;
        this.targetContainer = targetContainer;
        this.dropZone = dropZone;

        // Find jar target positions elements in DOM
        const divs:Element[] = Array.from(this.targetContainer.getElementsByClassName("epl_target_position"));

        // Generate jar target position object for  every target position DOM element
        divs.forEach( (e:Element) => {
            this.targetPositions.push(new JarTargetPosition( e as HTMLElement, this.targetContainer));
        });
    }

    /**
     * Generate request out of active bubbles
     * @returns EdupoGenRequest
     */
    public generateRequest():EdupoGenRequest
    {
        const req:EdupoGenRequest = new EdupoGenRequest();
        const params:any = {};

        this.activeIngredients.forEach( (b:Ingredient) => {
            params[b.parameter] = b.value;
        });

        req.fill(Settings.Instance.api_default_params);
        req.fill(params);

        return req;
    }    

    /**
     * Creates new ingredient object from ingredient settings
     * @param settings IngredientSettings
     * @returns Ingredient
     */
    public create(settings:IngredientSettings):Ingredient
    {
        if (!settings.color)
        {
            if (settings.parameter in Settings.Instance.colors)
            {
                settings.color = (Settings.Instance.colors as any)[settings.parameter];
            }            
        }
        let b:Ingredient = new TextBubble(this.dragContainer, text_bubble_html, settings);
        this.ingredients.push(b);
        return b;
    }

    /**
     * Start dragging an ingredient
     * @param b 
     */
    public drag(b:Ingredient)
    {
        // If ingredient was in the jar, unassign it from jar target position
        this.clearFromTarget(b);

        // Remove the ingredient from set of active ingredients if it was included in active ingredients.
        this.deactivate(b);

        // Bring visual element of ingredient forward and remove pointer events from other ingredients
        this.ingredients.forEach( (ing:Ingredient) => {            
            if (ing != b)
            {   
                ing.element.style.pointerEvents = 'none';                
                ing.element.style.zIndex = '0';
            }            
            else
            {
                ing.element.style.pointerEvents = 'auto';
                ing.element.style.zIndex = '1';
            }
        });
    }

    /**
     * Drop a dragged ingredient. Depending on the area of the drop, the ingredient is either
     * added to active ingredients or returned back to initial container for ingredients.
     */
    public drop(b:Ingredient)
    {
        // If the ingredient was dropped in the target zone
        if (this.isPointInside(new Point(b.x, b.y)))
        {
            this.animatedSnap(b).then(() => {
                this.activate(b);            
            });
        }
        else
        {
            this.deactivate(b);
            b.animatePosition(new Point(b.x, b.y), b.initialPosition);
        }        
        
        // Restore visual elements z order and restore pointer events
        this.ingredients.forEach( (ing:Ingredient) => {                        
                ing.element.style.pointerEvents = 'auto';
                ing.element.style.zIndex = '0';
        });
    }

    /**
     * Includes the ingredient into the set of active ingredients that will be used to form request.
     * If the active ingredients already contain an ingredient of the same type, the old one is replaced by the new one.
     * @param b Ingredient
     */
    public activate(b:Ingredient)
    {
        // Activate the ingredient
        b.active = true;
        if (!this.activeIngredients.includes(b))
            this.activeIngredients.push(b);

        // Deactivate conflicting ingredient and move it back to initial position
        this.ingredients.forEach( (a:Ingredient) => {
            if (a != b && (a.parameter == b.parameter) && (a.active))
            {
                this.deactivate(a);
                this.clearFromTarget(a);
                a.animatePosition(new Point(a.x, a.y), a.initialPosition);
            }            
        });
    }
    
    /**
     * Removes the ingredient from the set of active ingredient that will be used to form request.
     * @param b Ingredient
     */
    public deactivate(b:Ingredient)
    {
        b.active = false;        
        if (this.activeIngredients.includes(b))
            this.activeIngredients.splice(this.activeIngredients.indexOf(b),1);
    }

    /**
     * Sets initial positions of ingredients in the ingredients container. 
     * */
    public calculateInitialPositions()
    {
        // Randomize the order of ingredients. Can be turned on/off in settings.
        if (Settings.Instance.position_shuffle)
        {
            this.ingredients.forEach( (a:Ingredient) => {            
                let b = this.ingredients[randomInt(0, this.ingredients.length)];
                let tmpx:number = a.settings.x;
                let tmpy:number = a.settings.y;
                a.settings.x = b.settings.x;
                a.settings.y = b.settings.y;
                b.settings.x = tmpx;
                b.settings.y = tmpy;
            });
        }

        // Calculate screen positions from settings
        this.ingredients.forEach( (b:Ingredient) => {            
            b.initialPosition = this.calculateInitialPosition(b);
            b.x = b.initialPosition.x;
            b.y = b.initialPosition.y;
        });
    }

    /**
     * Calculates pixel position of the ingredient based on the normalized position defined in settings
     * and the rectangle of the source container.
     * @param b Ingredient
     * @returns Pixel position within drag container
     */
    private calculateInitialPosition(b:Ingredient):Point
    {
        const rect:DOMRect = this.sourceContainer.getBoundingClientRect();
        const crect:DOMRect = this.dragContainer.getBoundingClientRect();

        let p:Point = new Point(
            rect.left + rect.width * (b.settings.x  + Math.random() * Settings.Instance.position_jitter_x) - crect.left,
            rect.top + rect.height * (b.settings.y  + Math.random() * Settings.Instance.position_jitter_y) - crect.top
        );    

        return p;
    }

    /**
     * Updates initial positions and target positions for ingredients upon resize of window or container
     */
    public resize()
    {   
        // Recalculate initial pixel positions in ingredients container
        this.ingredients.forEach( (ing:Ingredient) => {
            ing.initialPosition.set( this.calculateInitialPosition(ing));
            if (!ing.active)
            {
                ing.x = ing.initialPosition.x;
                ing.y = ing.initialPosition.y;
            }            
        })        

        // Recalculate target positions in target container
        this.targetPositions.forEach( (p:JarTargetPosition) => {
            if (p.ingredient)
            {
                let tp:Point = new Point(p.x, p.y);
                tp = VisualElement.externalize(this.targetContainer.getBoundingClientRect(), tp);     
                tp = VisualElement.internalize(p.ingredient.element.parentElement!.getBoundingClientRect(), tp);       
                p.ingredient.x = tp.x;
                p.ingredient.y = tp.y;
                p.ingredient.basePosition = tp;
            }
        });        
    }
  
    /**
     * If the ingredient was assigned to a target position within jar, it clears the assignment,
     * thus making the target position vacant.
     * @param ing 
     */
    clearFromTarget(ing:Ingredient)
    {
        this.targetPositions.forEach( (p:JarTargetPosition) => {
            if (p.ingredient == ing)
            {
                p.ingredient = null;
            }
        });
    }    

    /**
     * Tests if a point (usually mouse position) lies within the drop area. 
     * The drop area is identified as #epl_jar_dropzone (TODO: refactor and assign in constructor)
     * 
     * @param p Point in screen coordinates
     * @returns True if the point lies within the drop area. False otherwise.
     */
    isPointInside(p:Point):boolean
    {        
        if (this.dropZone)
        {
            const rect:DOMRect = this.dropZone.getBoundingClientRect();
            const myrect:Rectangle = new Rectangle(rect.width, rect.height, rect.x, rect.y);
            return myrect.contains(p);
        }        
        return false;
    }    

    /**
     * Runs animation for putting a dragged ingredient inside the jar.
     * Finds a vacant position and starts the animation of snapping the ingredient to the position.
     * @param ing Dragged ingredient
     * @returns Promise resolved after the snapping animation finishes.
     */
    animatedSnap(ing:Ingredient):Promise<void>
    {
        // Find nearest vacant position
        let min:number = -1;
        let position!:JarTargetPosition;
        let ip:Point = VisualElement.externalize(ing.element.parentElement!.getBoundingClientRect(), new Point(ing.x, ing.y));
        this.targetPositions.forEach( (p:JarTargetPosition) => {
            if (!p.ingredient || p.ingredient.parameter == ing.parameter)
            {
                // Screen position of p
                let tp:Point = VisualElement.externalize(this.targetContainer.getBoundingClientRect(), new Point(p.x, p.y));
                
                // Calculate screen distance from target position to ingredient position
                let d = dist(tp.x, tp.y, ip.x, ip.y);
                if (min < 0 || d < min)
                {
                    min = d;
                    position = p;
                }
            }
        });

        // Assign the ingredient to the position
        if (position != null)
        {
            position.ingredient = ing;

            // Setup snapping animation:
            let tp:Point = new Point(position.x, position.y);
            tp = VisualElement.externalize(this.targetContainer.getBoundingClientRect(), tp);            
            if (ing.element.parentElement)
            {
                tp = VisualElement.internalize(ing.element.parentElement.getBoundingClientRect(), tp);
                return ing.animatePosition(new Point(ing.x, ing.y), new Point(tp.x, tp.y));
            }
        }
        else  // This should not happen
        {
            console.error("No vacant position in jar found! Is your number of ingredient categories higher than number of target positions?");
            
        }       
        return new Promise<void>((resolve) => {resolve();}); 
    }    
}