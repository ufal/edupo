import { Deserializable, Deserialize } from "../../fria/serialization";

export class IngredientSettings extends Deserializable
{
    @Deserialize()
    public parameter:string = '';

    @Deserialize()
    public label:string = '';

    @Deserialize()
    public value:string = '';

    @Deserialize()
    public x:number = 0;

    @Deserialize()
    public y:number = 0;

    @Deserialize()
    public color:string = "";

}