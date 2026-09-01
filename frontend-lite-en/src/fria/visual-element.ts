import { EventDispatcher } from "./event-dispatcher";
import { Point } from "./geometry";

/**
 * Extension of HTMLElement with useful methods regarding positioning, mouseinteraction etc.
 * At this point of development, VisualElement is assumed to be positioned absolutely.
 * Other positining mode might come in future, but most probably not.
 * 
 * Visual element is positioned absolutely within its parent;
 * Either in normalized nx,ny coordinates (0..1) x (0..1)
 * or in screen coordinates x,y (0..parent.clientwidth) x (0..parent.clientHeight)
 */
export class VisualElement
{
    parent:HTMLElement|null = null;
    width: number = 0;
    height: number = 0;
    element!: HTMLElement;
    events!:EventDispatcher;

    public get x():number           { return this.element.offsetLeft; }
    public set x(value:number)      { this.element.style.left = value + "px"; }
    public get nx():number          { return (this.parent) ? this.element.offsetLeft / this.parent.clientWidth: 0; }    
    public set nx(value:number)     { if (this.parent) this.element.style.left = value * this.parent.clientWidth + "px"; }

    public get y():number           { return this.element.offsetTop; }
    public set y(value:number)      { this.element.style.top = value + "px";}
    public get ny():number          { return (this.parent) ? this.element.offsetTop / this.parent.clientHeight: 0; }    
    public set ny(value:number)     { if (this.parent) this.element.style.top = value * this.parent.clientHeight + "px"; }

    public get position():Point       { return new Point(this.x, this.y);}

    constructor (element:HTMLElement, parent:HTMLElement|null = null)
    {
        this.element = element;
        this.parent = parent;    
        this.events = new EventDispatcher();    
    }

    /**
     * Changes the parent of this visual element, while maintaining visual position
     * @param newparent 
     */
    reparent(newparent:HTMLElement)
    {
        if (this.parent)
        {
            // Calculate screen position
            let sp:Point = VisualElement.externalize(this.parent.getBoundingClientRect(), this.position);

            // Convert screen to local coordinates within new parent
            sp = VisualElement.internalize(newparent.getBoundingClientRect(), sp);

            newparent.appendChild(this.element);
            this.parent = newparent;
            this.x = sp.x;
            this.y = sp.y;
        }
    }

    /**
     * Converts position or translation vector from pixel coordinates to normalized internal coordinates
     * @param p 
     * @returns 
     */
    normalize(p:Point):Point
    {
        return p.divXY(this.element.clientWidth, this.element.clientHeight);
    }

    /**
     * Converts position or translation vector from normalized internal coordinates to pixel coordinates
     * @param p 
     * @returns 
     */    
    denormalize(p:Point):Point
    {
        return p.mulXY(this.element.clientWidth, this.element.clientHeight);
    }

    /**
     * Converts screen (world) position to internal pixel coordinates
     * @param p 
     * @returns 
     */    
    static internalize(rect:DOMRect, p:Point = Point.Zero):Point
    {
        // Screen rectangle of container
        //let rect = this.element.getBoundingClientRect();       
        return new Point(p.x - rect.left, p.y - rect.top);
    }

    /**
     * Converts internal pixel coordinates to screen (world) position
     * @param p 
     * @returns 
     */
    static externalize(rect:DOMRect, p:Point = Point.Zero):Point
    {
        // Screen rectangle of container
        //let rect = this.element.getBoundingClientRect();       
        return new Point(rect.left + p.x, rect.top + p.y);
    }

    /**
     * Converts position from client coordinates to internal normalized coordinates
     * @param clientX MouseEvent.clientX
     * @param clientY MouseEvent.clientY
     */
    internalMousePosition(clientX:number, clientY:number):Point
    {
        // Screen rectangle of container
        let rect = this.element.getBoundingClientRect();

        // Offset of mouse from container upper left corner
        let offset:Point = this.normalize(new Point(clientX - rect.left, clientY - rect.top));

        return offset;
    }
}