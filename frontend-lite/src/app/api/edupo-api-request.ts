import { Deserializable, Deserialize } from "../../fria/serialization";

/**
 * Data structure for sending API requests to Edupo API
 */
export class EdupoGenRequest extends Deserializable
{
    @Deserialize()
    public modelspec:string = "tm";

    @Deserialize()
    public poem_length:string = "";

    @Deserialize()
    public rhyme_scheme:string = "";

    @Deserialize()
    public verses_count: number = 0;
    
    @Deserialize()
    public syllables_count: number = 0;

    @Deserialize()
    public motives:string = "";

    @Deserialize()
    public mood:string = "";

    @Deserialize()
    public old_style:string = "";

    @Deserialize()
    public rhymed:string = "";

    @Deserialize()
    public temperature:number = 0.7;

    // @Deserialize()
    // public metre: string = "";

    // @Deserialize()
    // public first_words:string[] = [];

    // @Deserialize()
    // public anaphors: number = 0;

    // @Deserialize()
    // public epanastrophes:number = 0;

    // @Deserialize()
    // public temperature: number = 0.7;

    // @Deserialize()
    // public max_strophes:number = 0;

    // @Deserialize()
    // public title: string = "";

    // @Deserialize()
    // public author_name: string = "";

    // @Deserialize()
    // public form:string = "";

    // @Deserialize()
    // public min_meaning:number = 0.7;
    
    // @Deserialize()
    // public max_unk: number = 0.05;

    // @Deserialize()
    // public max_tries: number = 1;

    public urlEncode():string
    {
        return new URLSearchParams(this.toObject()).toString();
    }
}