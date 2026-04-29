import { EdupoAPI } from "../api/edupo-api";
import { EdupoGenRequest } from "../api/edupo-api-request";
import { GeneratorState } from "./constants";

/**
 * Implements logic related to poem generation.
 * Receives input parameters for poem generation from visual interface.
 * Performs validation of parameters.
 * Contacts EdupoAPI to generate poems.
 * Sends generated output to visual interface.
 */
export class Generator
{
    private api:EdupoAPI
    public request!:EdupoGenRequest;
    public state:string = GeneratorState.STATE_IDLE;

    constructor(api:EdupoAPI)
    {
        this.api = api;     
        this.reset();   
    }

    public async generate():Promise<any>
    {
        this.state = GeneratorState.STATE_PROCESSING;        
        return this.api.gen(this.request).then( ()=> { this.state = GeneratorState.STATE_FINISHED});
    }

    public reset()
    {
        this.request = new EdupoGenRequest();
    }    
}

