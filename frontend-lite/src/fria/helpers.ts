export function clamp(value: number, min: number, max: number): number
{
    return Math.min(Math.max(value, min), max);
}

export function random(min: number, max: number): number
{
    return Math.random() * (max - min) + min;
}

export function randomInt(min: number, max: number): number
{
    return Math.floor(random(min, max));
}

export function map(value:number, source_min:number, source_max:number, target_min:number, target_max:number):number
{
    if (source_min == source_max) 
        return value;
    else
        return target_min + (value - source_min) / (source_max - source_min) * (target_max - target_min);
}

export function dist(x1:number, y1:number, x2:number, y2:number ): number
{
    return Math.sqrt( Math.pow(x2-x1,2) + Math.pow(y2-y1,2));
}

export function className(obj:any):string
{
    return (obj as any).constructor.name;
}

/**
 * Reads SVG file url from 'data-svg' attribute and injects the content of the SVG file into the element
 * @param element 
 * @param data Alternative name for the 'data-svg' attribute, without the 'data-' prefix
 * @returns 
 */
export function inject_svg(element:HTMLElement, data:string = "svg"):Promise<string|void>
{
    // Find SVG src
    const svg_url:string = element.dataset[data] as string;

    // Load the content
    return fetch(svg_url).then(r => r.text()).then(svg => {element.insertAdjacentHTML("afterbegin", svg)});    
}

