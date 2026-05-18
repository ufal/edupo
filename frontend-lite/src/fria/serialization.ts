/**
 * Implements logic for deserialization of typed objects from anonymous objects (e.g. from JSON files)
 *
 * Classes extending this class gain a static method FromObject(obj) which constructs a new typed object from the given
 * anonymous object and toObject() method which serializes the typed object into a new anonymous object.
 *
 * Class properties marked by @Deserialize(options) decorator will be used in (de-)serialization, other properties are ignored.
 *
 * The decorator is configurable by an optional parameter object with the following properties
 * - type : any             Class prototype used in deserialization. If not defined, the value is simply copied from anonymous object.
 * - isArray: boolean       True if the class property should be deserialized as an array. Default is false.
 * - from: string           Name of property in source anonymous object if it's different than the name of the target property.
 *
 */
export class Deserializable
{
    public clone():any
    {
        return (this.constructor as any)['FromObject'](this.toObject());
    }

    public fill(input:any):any
    {
        let optionsDictionary = this.constructor.prototype['_propOptions'];
        
        let me = this as any;

        if (optionsDictionary)
        {
            for (let outKey in optionsDictionary)
            {
                if (optionsDictionary.hasOwnProperty(outKey))
                {
                    let options = optionsDictionary[outKey];

                    // Import value from anonymous object
                    let inKey = (options && ('from' in options) && options['from']) ? options['from'] : outKey;
                    let outType = (options && ('type' in options)) ? options['type'] : null;

                    if (input.hasOwnProperty(inKey) && input[inKey] !== null && typeof input[inKey] !== "undefined")
                    {
                        if (outType != null)
                        {
                            // If the value is an array of defined type
                            if (options.isArray)
                            {
                                // New blank array is created
                                me[outKey] = [];

                                // Output array filled one by one by deserialization of input array values
                                for (let i = 0; i < input[inKey].length; i++)
                                {
                                    if (input[inKey][i] !== null && typeof input[inKey][i] !== "undefined")
                                    me[outKey][i] = (outType).FromObject(input[inKey][i]);
                                }
                            }
                            else
                            {
                                // Value is filled by deserialization of input value
                                me[outKey] = (outType).FromObject(input[inKey]);
                            }
                        }
                        else
                        {
                            // If type is not defined the value is simply copied
                            if (typeof me[outKey] == 'object' && !Array.isArray(me[outKey]) && Array.isArray(input[inKey]) && input[inKey].length == 0)
                            {
                                // A frustrated fix required in cases when object {} is wrongly serialized in JSON as array []. Yes, these things happen :(
                                me[outKey] = {};
                            }
                            else me[outKey] = input[inKey];
                        }
                    }
                }
            }
        }
        return this;
    }

    static FromObject(input:any):any
    {
        let output = new this();
        output.fill(input);
        return output;
    }

    public toObject()
    {
        let obj:any = {};
        let me = this as any;

        let optionsDictionary = this.constructor.prototype['_propOptions'];

        if (optionsDictionary)
        {
            for (let inKey in optionsDictionary)
            {
                if (optionsDictionary.hasOwnProperty(inKey))
                {
                    let options = optionsDictionary[inKey];
                    let outKey = (options && ('from' in options) && options['from']) ? options['from'] : inKey;

                    if (this.hasOwnProperty(inKey) && me[inKey] !== null && typeof me[inKey] !== "undefined")
                    {
                        let options = optionsDictionary[inKey];

                        if (options && options.isArray)
                        {
                            obj[outKey] = [];

                            for (let i = 0; i < me[inKey].length; i++)
                            {
                                if (me[inKey][i] != null)
                                    obj[outKey][i] = me[inKey][i].toObject();
                                else
                                    obj[outKey][i] = null;
                            }
                        }
                        else
                        {
                            if (typeof me[inKey]['toObject'] === 'function')
                                obj[outKey] = me[inKey].toObject();
                            else
                                obj[outKey] = me[inKey];

                        }
                    }
                }
            }
        }
        return obj;
    }
}

export function Deserialize(options?:DeserializationOptions)
{
    return function (target: any, key: string) {

        // Define property deserialization options on class if it's not defined yet
        if (Object.getOwnPropertyDescriptor(target, '_propOptions') == null)
        {
            // Create internal JSON options
            Object.defineProperty(target, '_propOptions', {
                enumerable: true,
                configurable: true,
                value: {},
                writable: true
            });

            // Inherit JSON options from parent class
            let parentTarget = Object.getPrototypeOf(target);
            let parentData = parentTarget['_propOptions'];
            if (parentData) {
                for (let parentKey in parentData)
                {
                    if(parentData.hasOwnProperty(parentKey))
                        if (!target['_propOptions'].hasOwnProperty(parentKey))
                            target['_propOptions'][parentKey] = parentData[parentKey];
                }
            }
        }

        // Store deserialization options for this property
        target['_propOptions'][key] = options;        
    }
}

interface DeserializationOptions
{
    type?:any;
    isArray?:boolean;
    from?:string;
}