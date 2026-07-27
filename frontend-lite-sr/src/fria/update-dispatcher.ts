import { Time } from "./time";
import type { Updatable } from "./updatable";

export class UpdateDispatcher
{    
    private static updatables:Updatable[] = [];
    private static running:boolean = false;    
    private static paused:boolean = false;

    public static Add(updatable:Updatable):void
    {
        if (this.updatables.indexOf(updatable) < 0)
        {
            this.updatables.push(updatable);
            updatable.start();
        }

        if (!this.running)
        {
            this.Loop();
        }
    }

    public static Remove(updatable:Updatable):void
    {
        let i = this.updatables.indexOf(updatable);
        if (i >= 0)
        {
            this.updatables.splice(i, 1);
        }
    }

    private static Loop(currentTime:DOMHighResTimeStamp = 0)
    {
        if (currentTime > 0 && !this.paused)
        {
            for (let i = 0; i < this.updatables.length; i++ )
            {
                let u:Updatable = this.updatables[i];
    
                if (u.width != u.element.clientWidth || u.height != u.element.clientHeight)
                {
                    u.width = u.element.clientWidth;
                    u.height = u.element.clientHeight;
                    u.resize();
                }
    
                if (!Time.paused && Time.update(currentTime))       
                {
                    this.updatables[i].update();
                }
            }    
        }

        requestAnimationFrame( (time) => { UpdateDispatcher.Loop(time);});
    }
    
    public static Pause()
    {
        this.paused = true;
    }

    public static Unpause()
    {
        this.paused = false;
    }

}