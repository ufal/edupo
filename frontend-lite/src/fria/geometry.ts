/**
 * Basic class for two-dimensional point and some operations with it
 */
export class Point
{
    public x:number = 0.0;
    public y:number = 0.0;
    public z:number = 0.0

    /**
     * Option to attach arbitrary data to the point
     */
    public data:any = {};

    constructor(x:number = 0, y:number = 0, z:number = 0)
    {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    static get Zero():Point { return new Point(0,0,0);}
    static get One():Point {return new Point(1,1,1);}

    add(b:Point):Point              { return new Point(this.x + b.x, this.y + b.y, this.z + b.z); }
    addXY(x:number, y:number):Point { return new Point(this.x + x, this.y + y);}
    subXY(x:number, y:number):Point { return new Point(this.x - x, this.y - y);}
    sub(b:Point):Point              { return new Point(this.x - b.x, this.y - b.y, this.z - b.z); }
    lerp(b:Point, t:number):Point   { return new Point((1-t) * this.x + t * b.x, (1-t) * this.y + t * b.y, (1-t) * this.z + t * b.z); }
    len():number                    { return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z); }
    mul(s:number):Point             { return new Point(this.x * s, this.y * s, this.z * s); }
    mulXY(x:number, y:number):Point { return new Point(this.x * x, this.y * y); }
    divXY(x:number, y:number):Point { return new Point(this.x / x, this.y / y); }
    dot(b:Point):number             { return this.x * b.x + this.y * b.y + this.z * b.z; }
    norm():Point                    { return this.mul(1.0/this.len())}
    scale(b:Point):Point            { return new Point(this.x * b.x, this.y * b.y, this.z * b.z);}
    clone():Point                   { return new Point(this.x, this.y, this.z);}
    set(b:Point):Point              { this.x = b.x; this.y = b.y; this.z = b.z; return this;}
}

/**
 * Simple immutable rectangle structure
 */
export class Rectangle
{
    /** Width of rectangle */
    public get width():number {return this._width}
    private _width:number;

    /** Height of rectangle */
    public get height():number {return this._height}
    private _height:number;

    /** Normalized coordinates of pivot point within rectangle */
    public get pivot():Point {return this._pivot.clone()};
    private _pivot:Point = new Point(0,0);

    /** Position of the rectangle */
    public get position():Point {return this._position.clone()}
    private _position:Point = new Point(0,0);

    public get left():number { return this.position.x - this.width * this.pivot.x }
    public get top():number { return this.position.y - this.height * this.pivot.y }    
    public get right():number { return this.left + this.width }
    public get bottom():number { return this.top + this.height }
    public get aspect_ratio():number {return this.width/this.height}
    
    constructor (width:number, height:number, x:number = 0, y:number = 0, pivot_x:number = 0, pivot_y:number = 0)
    {
        this._width = width;
        this._height = height;
        this._position = new Point(x,y);
        this._pivot = new Point(pivot_x, pivot_y);
    }

    clone():Rectangle
    {
        return new Rectangle(this.width, this.height, this.position.x, this.position.y, this.pivot.x, this.pivot.y);
    }

    contains(P:Point):boolean
    {
        if (this.width > 0 && this.height > 0)
        {
            const rx = P.x - this.left;
            const ry = P.y - this.top;
            return (rx > 0 && rx < this.width && ry > 0 && ry < this.height);
        }
        else return false;
    }
}
