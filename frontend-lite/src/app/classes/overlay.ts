import { clamp, map } from "../../fria/helpers";
import { Time } from "../../fria/time";
import type { Updatable } from "../../fria/updatable";

/**
 * Manages showing and hiding modal interaction-blocking overlay that is displayed 
 * while the application waits for asynchronous operations to finish.
 * Overlay is accessible from anywhere in code through static singleton and its Show() and Hide() methods.
 */
export class Overlay implements Updatable
{
    element!:HTMLElement; 

    /**
     * Semaphore counter tracking if the overlay should be visible or not.
     * Everybody calling Overlay.show() must also call Overlay.hide() to release the semaphore.
     */
    private showcounter:number = 0;

    /**
     * Animated progress bar image. 
     */
    private progressbar!:HTMLImageElement;

    public static Instance:Overlay;

    private progress:number = 0;

    private images:string[] = ["00","10","20","30","40","50","60","70","80","90","100"];

    public width: number = 0;
    public height: number = 0;

    public static Initialize(el:HTMLElement|null):Overlay
    {
        if (!this.Instance)
            this.Instance = new Overlay(el);

        return this.Instance;
    }

    constructor (el:HTMLElement|null)
    {
        this.element = el as HTMLElement;
        this.progressbar = document.getElementById("epl_waiting_progress") as HTMLImageElement;
    }
    
    start(): void
    {
        // Preload images
        for (let i = 0; i < this.images.length; i++)
        {
            const img=new Image();
            img.src=this.getImageName(1.0 / this.images.length * i);
        }
    }

    resize(): void
    {
        
    }

    update(): void {

        if (this.element.style.visibility == "visible")
        {
            this.progressbar.src = this.getImageName(this.progress);
            this.progress = map(Math.sin(Time.time * 10), -1, 1, 0.0, 0.8);
        }
    }

    public static Show()
    {
        this.Instance.element.style.visibility = "visible";
        this.Instance.element.classList.add("fadein_1s");
        this.Instance.showcounter++;
    }

    public static Hide()
    {
        if (--this.Instance.showcounter <= 0 )
        {
            this.Instance.element.style.visibility = "hidden";
            this.Instance.element.classList.remove("fadein_1s");
            this.Instance.element.offsetHeight;
            this.Instance.showcounter = 0;
        }        
    }

    private getImageName(progress:number):string
    {
        let index = Math.ceil(10.0 * progress);
        index = clamp(index, 0, this.images.length);
        return `assets/progress_${this.images[index]}.png`;
    }
}