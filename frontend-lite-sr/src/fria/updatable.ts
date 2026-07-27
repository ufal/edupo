/**
 * Interface for objects representing visual elements with interactive/animated properties.
 * Updatable objects need to be added to UpdateDispatcher singleton which automatically calls
 * their start/resize/update methods when needed.
 */
export interface Updatable
{
    /**
     * The visual element connected to this updatable. Not its parent or container.
     */
    element:HTMLElement;

    /**
     * Width of the element, in pixels
     */
    width:number;

    /**
     * Height of the element, in pixels
     */
    height:number;

    /**
     * Called once, when the updatable is added to the update cycle
     */
    start():void;

    /**
     * Called when the width or height is different from the element.clientWidth or element.clientHeight.
     * Update dispatcher automatically updates width and height to clientWidth and clientHeight before call to resize().
     */
    resize():void;

    /**
     * Called each frame while Time is running.
     */
    update():void;
    
}