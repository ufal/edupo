import { EventDispatcher } from "../../fria/event-dispatcher";
import { Point } from "../../fria/geometry";
import { clamp } from "../../fria/helpers";
import { Time } from "../../fria/time";
import { Easing, Tween } from "../../fria/tween";
import type { Updatable } from "../../fria/updatable";
import { VisualElement } from "../../fria/visual-element";
import { Settings } from "../settings";
import type { IngredientSettings } from "./ingredient-settings";

/**
 * Base class for ingredients. Each ingredient is visually represented as a bubble.
 * Specific classes (e.g. bubble with text, bubble with image icon, etc.) should be derived from this base class
 */
export class Ingredient extends VisualElement implements Updatable
{
    public value:string|number ="";
    public label:string = "";
    public parameter:string = "";
    public settings!:IngredientSettings;

    private template:string = "";
       
    private isDragged:boolean = false;

    // Distance while dragging between position of drag start and current position    
    private pointerDelta:Point = Point.Zero;

    // Position of mouse pointer when drag started
    private oldPointerPosition:Point = Point.Zero;

    // Screen x,y position of the ingredient when drag started
    private oldElementPosition:Point = Point.Zero;
    
    // Normalized position within initial rectangle. 
    // This is the position that bubble will return to when removed from jar.
    // The position is set by manager using setInitialPosition()
    public initialPosition:Point = new Point(0.5, 0.5);

    // Position of the bubble (in screen coordinates). 
    // The actual x,y, position might be slightly different because the bubble might oscillate during animation around this position
    public basePosition:Point = Point.Zero;
    
    
    private pointerMoveHandler!:(e:PointerEvent) => any;
    private pointerOutHandler!:(e:PointerEvent) => any;

    // Active bubbles are those that are inserted into active area in app
    private _active:boolean = false;
    public get active():boolean {return this._active};
    public set active(v:boolean) {this.setActive(v);}

    /* Animation */
    private positionTween:Tween<Point>|null = null;
    private animationRunning:boolean = false;
    private animationOffset:number = Math.random();

    constructor (parent:HTMLElement, template:string, settings:IngredientSettings)
    {                
        super(document.createElement("div"), parent);   
    
        this.template = template;
        this.settings = settings;
        this.parameter = this.settings.parameter;
        //this.initialPosition = new Point(this.settings.x, this.settings.y);
        this.value = this.settings.value;
        this.label = this.settings.label;

        this.parent?.appendChild(this.element);

        this.element.addEventListener("pointerdown", this.onPointerDown.bind(this));
        this.element.addEventListener("pointerup", this.onPointerUp.bind(this));
        this.pointerMoveHandler = this.onPointerMove.bind(this);
        this.pointerOutHandler = this.onPointerUp.bind(this);
        this.events = new EventDispatcher();

        this.element.innerHTML = this.template;
        this.element.className = "epl_bubble";     
        this.element.classList.add(this.settings.parameter);
        if (settings.color)
        {
            this.element.style.backgroundColor = settings.color;
        }
        this.updateValue();
    }

    start(): void {                                

    }

    update(): void {
        this.clamp();         

        if (this.animationRunning)
        {
            if (this.positionTween)
            {
                this.positionTween.update(Time.deltaTime);
            }            
        }

        // Up and down bobbling animation in active state
        if (this.active && !this.isDragged)
        {
            const offset = new Point(0, Math.sin((Time.time - this.animationOffset)* 1.5) * 20 );
            // const transform = `translate(${offset.x}px, ${offset.y}px)`;
            // console.log(transform);
            // this.element.style.transform = transform;
            const pos = this.basePosition.add(offset);
            this.x = pos.x;
            this.y = pos.y;
        }
    }

    resize(): void {
    }

    clamp():void
    {
        if (this.parent)
        {
            this.x = clamp(this.x, this.width/2, this.parent.clientWidth - this.width/2);
            this.y = clamp(this.y, this.height/2, this.parent.clientHeight - this.height/2);
        }
    }

    onPointerDown(e:MouseEvent)
    {
        if (this.animationRunning) return;

        if (!this.isDragged)
        {
            this.events.dispatchEvent("dragstart", this);
            this.oldPointerPosition = new Point(e.clientX, e.clientY);
            this.oldElementPosition = new Point(this.x, this.y);
            this.pointerDelta = Point.Zero;
            this.isDragged = true;
            this.parent?.addEventListener("pointermove", this.pointerMoveHandler);
            this.parent?.addEventListener("pointerleave", this.pointerOutHandler);
        }        
    }

    onPointerUp()
    {
        if (this.animationRunning) return;

        if (this.isDragged)
        {
            this.events.dispatchEvent("dragend", this);
            this.basePosition = new Point(this.x, this.y);
            this.animationOffset = Time.time;
        }
        this.isDragged = false;
        this.parent?.removeEventListener("pointermove", this.pointerMoveHandler);
        this.parent?.removeEventListener("pointerleave", this.pointerOutHandler);
    }

    animatePosition(from:Point, to:Point):Promise<void>
    {
        const result:Promise<void> = new Promise<void>((resolve) => {

            this.animationRunning = true;
            const duration = from.sub(to).len() / Settings.Instance.animation_speed;
            this.positionTween = new Tween<Point>(from, to, duration, Easing.EASE_IN_OUT,
                (v:Point) => {
                                this.x = v.x;
                                this.y = v.y;
                             }, 
                () => {
                    this.animationRunning = false;
                    resolve();
                });
        });

        return result;
    }

    onPointerMove(e:PointerEvent)
    {
        if (this.animationRunning) return;

        if (this.isDragged)
        {
            let pointer:Point = new Point(e.clientX, e.clientY);
            this.pointerDelta= pointer.sub(this.oldPointerPosition);
            let newPosition:Point = this.oldElementPosition.add(this.pointerDelta);

            this.x = newPosition.x;
            this.y = newPosition.y;
        }
    }

    updateValue()
    {        
        let valElement = this.element.getElementsByClassName("epl_bubble_value")[0];
        if (valElement)
        {
            valElement.innerHTML = this.label.toString();
        }
        else
        {
            console.error("Value element not found");
        }
        
    }

    setActive(isActive:boolean)
    {
        this._active = isActive;
        if (this.active)
        {
            this.element.classList.add("active");
            this.element.classList.remove("passive");
            this.basePosition = new Point(this.x, this.y);
        }
        else
        {
            this.element.classList.remove("active");
            this.element.classList.add("passive");
        }
    }
}