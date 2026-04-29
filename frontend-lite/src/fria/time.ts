/**
 * Singleton class for reading time values in each frame.
 * Time values are derived from DOMHighResTimeStamp and converted to seconds.
 * Updating time values is called by UpdateDispatcher.
 * 
 * Time class also allows for a special mode: fake FPS. In fake FPS mode, 
 * time values are not derived from actual time, but increased in each update by 1.0/fakeFPS. 
 * Thus, animation runs in even time steps, even though visual framerate might be different.
 * This is used to generate still frames to be assembled into video.
 */
export class Time
{
    /**
     * Absolute time at the start of application
     */
    static originTime:number = 0;
    
    /**
     * Current absolute time
     */
    static time:number = 0;

    /**
     * Time difference between current time and the time in previous frame
     */
    static deltaTime:number = 0;

    /**
     * Absolute time in previous frame
     */
    static lastTime:number = 0;

    /**
     * Current value of frames per second. Calculating from the last 1 second.
     */
    static fps:number = 0;

    /**
     * Setting paused to true stops UpdateDispatcher from updating
     */
    static paused:boolean = false;    

    /**
     * Total number of frames since start of application
     */
    static frame:number = 0; 

    /**
     * This parameter enables a special mode in which deltaTime is not calculated from real time but it's faked to be equal to 1.0/fakeFPS.
     * This is used for capturing videos where each frame rendered in real-time corresponds to 1 video frame.
     */
    static fakeFPS:number = 0;

    private static fpsCounter = 0;
    private static fpsCountTimer = 0;
    private static lastFrame = 0;
    private static fpsLimit = 0;

    public static update(t:DOMHighResTimeStamp)
    {
        this.time = 0.001 * t;

        if (this.originTime == 0)  // first run
        {
            this.lastTime = this.originTime = this.lastFrame = this.time;
        } 
        else
        {
            if (this.time == this.lastTime) return true;
            
            this.deltaTime = this.time - this.lastTime;

            if (this.fakeFPS)
            this.deltaTime = 1.0 / this.fakeFPS;

            this.lastTime = this.time; 
            this.fpsCountTimer += this.deltaTime;
        
            let doRender = false;
        
            if (this.fpsLimit == 0)
                doRender = true;
            else
            {
                let sinceLast = this.time - this.lastFrame;
                if (sinceLast >= 1.0 / this.fpsLimit)
                {
                    doRender = true;
                    this.lastFrame = this.time;    
                }
            }
        
            if (doRender)
            {
                this.frame++;

                this.fpsCounter++;

                if (this.fpsCountTimer > 1)
                {
                    this.fps = this.fpsCounter / this.fpsCountTimer;
                    this.fpsCounter = 0;
                    this.fpsCountTimer -= 1;    
                }
            }
        
            return doRender;    
        }
        return true;
    }
}