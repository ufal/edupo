import { Overlay } from "../classes/overlay";
import { EdupoGenRequest } from "./edupo-api-request";
import { EdupoGenResponse } from "./edupo-gen-response";

export class EdupoAPI
{
    private url:string = "";
    
    constructor(api_url:string)
    {
        this.url = api_url;
    }

    /**
     * General API request. Doesn't process the response any further than converting JSON to anynoymous object
     * @param endpoint 
     * @param data 
     * @returns 
     */
    private async request(endpoint:string, data:EdupoGenRequest|null = null):Promise<any>
    {
        // NOTE: EdupoAPI doesn't support JSON data in request body. URL-encoded FormData needs to be used instead
        
        let body:string = "";
        if (data)
        {
            body =  data.urlEncode();
        }

        Overlay.Show();

        const response = await fetch(this.url + "/" + endpoint,
        {
            
            method: "POST",
            headers: { 
                "Content-Type": "application/x-www-form-urlencoded",
                "accept":"application/json" 
            },
            body:body
        });

        if (!response.ok) {
            // Throw an error with status info
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorText}`);        
        }
        
        return response.json().finally( ()=>{ Overlay.Hide();} ) as Promise<any>;        
    }

    public async test(): Promise<any>
    {
        return this.request('prdel');
    }

    /**
     * Calls 'generate' endpoint of API and transforms the response to EdupoGenResponse
     * @param request 
     * @returns 
     */
    public async gen(request:EdupoGenRequest): Promise<EdupoGenResponse>
    {
        return this.request('gen', request).then( (response:any) => {
                const result:EdupoGenResponse = new EdupoGenResponse();
                result.fill(response);
                return result;
        });
    }
}