import type { Point } from "./geometry";
import { className } from "./helpers";

/**
 * Named constants for types of tweening
 */
export class Easing
{
    public static readonly LINEAR:string = "linear";
    public static readonly EASE_IN_OUT:string = "inout";
}

/**
 * Tweening class for animation. Tween currently supports scalar numbers (e.g. opacity) and Points (e.g. 2D/3D position).
 * Tween calls its updated() callback on each update and its finished() callback after finishing.
 * Tween progresses each time its update() method is called. This needs to be called in script, 
 * usually within the update() method of the visual element which instantiated the tween.
 * 
 * The code is inspired by Jeff Johnson's Tween for Unity: https://assetstore.unity.com/packages/tools/animation/tween-55983
 */
export class Tween<T>
{
    public from:T;
    public to:T;
    public duration:number = 1;
    public time:number = 0;
    public delay:number = 0;
    public easing:string = Easing.LINEAR;

    public get finished() {return this._finished;};
    private _finished = false;

    private onUpdated:(value:T) => void = () => {};
    private onFinished:() => void = () => {};

    public static SmoothStep(t:number):number
    {
        if (t < 0) t = 0;
        if (t > 1) t = 1;

        return  t * t * (3.0 - 2.0 * t);
    }
    
    public constructor(from:T, to:T, duration:number, easing:string = Easing.LINEAR, updated?: (value:T) => void, finished?: () => void)
    {
        this.from = from;
        this.to = to;
        this.easing = easing;

        if (typeof duration != "undefined") this.duration = duration;
        if (typeof updated != "undefined") this.onUpdated = updated;
        if (typeof finished != "undefined") this.onFinished = finished;
    }

    public value():T
    {
        let t:number = this.time / this.duration;

        switch (this.easing)
        {
            case Easing.EASE_IN_OUT:
                 t = Tween.SmoothStep(t);
                 break;

            case Easing.LINEAR:
            default:
                t = t;
        }

        if (typeof this.from == "number" && typeof this.to == "number")
        {
            let from:number = this.from as number;
            let to:number = this.to as number;

            return ((1 - t) * from + t * to) as unknown as T;
        }        
        else if (className(this.from) == "Point")
        {
            let from:Point = this.from as Point;
            let to:Point = this.to as Point;

            return from.lerp(to, t) as unknown as T;
        }
        else
        {
            console.error("Uknown tween type: " + className(this.from));
        }        
        return undefined as T;
    }

    public update(deltaTime:number)
    {
        this.time += deltaTime;

        if (this.time < this.duration)
        {
            if (this.onUpdated) this.onUpdated(this.value());
        }
        else
        if (this.time >= this.duration)
        {
            this.time = this.duration;
            this._finished = true;
            if (this.onUpdated) this.onUpdated(this.to);
            if (this.onFinished) this.onFinished();
        }            

        if (this.time < 0)            
            this.time = 0;
    }

    public reset()
    {
        this.time = 0;
        this._finished = false;
    }
}