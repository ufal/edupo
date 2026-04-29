import { VisualElement } from "../../fria/visual-element";
import type { Ingredient } from "./ingredient";

export class JarTargetPosition extends VisualElement
{
    public ingredient:Ingredient|null = null;
}