import { Deserializable, Deserialize } from "../../fria/serialization";

export class EdupoGenResponse extends Deserializable
{
    @Deserialize()
    public author_name:string = "";

    @Deserialize()
    public id:string = "";

    @Deserialize()
    public plaintext:string = "";

    @Deserialize()
    public rawtext:string = "";

    @Deserialize()
    public title:string = "";

    public lines():string[]
    {
        return this.plaintext.split('\n');
    }

}
