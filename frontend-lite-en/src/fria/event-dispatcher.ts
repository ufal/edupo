/**
 * Adds custom events to any object
 */
export class EventDispatcher
{
    protected eventHandlers:any = {};

    public addEventListener(eventName:string, fn: (...args:any) => any)
    {
        if (!(eventName in this.eventHandlers))
        {  
            this.eventHandlers[eventName] = [];
        }

        this.eventHandlers[eventName].push(fn);
    }

    public removeEventListener(eventName:string, fn: (...args:any) => any)
    {
        if (!(eventName in this.eventHandlers)) return;

        for (let i = 0; i < this.eventHandlers[eventName].length; i++)
        {
            if (this.eventHandlers[eventName][i] == fn)
            {
                this.eventHandlers[eventName] = this.eventHandlers[eventName].splice(i,1);
                break;
            }
        }
    }

    public dispatchEvent(eventName:string, ...args:any)
    {
        if (eventName in this.eventHandlers)
        {
            this.eventHandlers[eventName].forEach( ( fn:(...args:any)=>any) => {
                fn(args);
            });
        }
    }
}