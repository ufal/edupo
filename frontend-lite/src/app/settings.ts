import { Deserializable, Deserialize } from "../fria/serialization";
import { IngredientSettings } from "./classes/ingredient-settings";

export class SerializablePoint extends Deserializable
{
    @Deserialize()
    public x:number = 0;

    @Deserialize()
    public y:number = 0;
}

export class Settings extends Deserializable
{
    @Deserialize()
    public app_version:string = '1.0';

    @Deserialize()
    public api_url:string = 'https://quest.ms.mff.cuni.cz/edupo-api/';

    @Deserialize()
    public api_default_params:object = {};

    @Deserialize()
    public animation_speed:number = 1.0;

    @Deserialize()
    public share_url:string = 'https://quest.ms.mff.cuni.cz/edupo-api/show?poemid={0}';

    @Deserialize()
    public colors:object = {};

    @Deserialize({isArray:true, type:IngredientSettings})
    public ingredients:IngredientSettings[] = [];

    @Deserialize()
    public position_jitter_x:number = 0;
    
    @Deserialize()
    public position_jitter_y:number = 0;

    @Deserialize()
    public position_shuffle:boolean = false;

    @Deserialize({isArray:true, type:SerializablePoint})
    public target_points:SerializablePoint[] = [];

    public static Instance:Settings;

    public constructor()
    {
        super();
        Settings.Instance = this;
    }



}