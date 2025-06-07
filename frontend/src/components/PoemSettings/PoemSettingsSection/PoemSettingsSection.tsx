import * as React from "react"

import { Switch } from "../../ui/switch";
import Title from "./PoemSettingsTitle";
import Flag from "./PoemSettingsFlag";
import { PoemSettingsFlagMessage } from "./PoemSettingsFlag/PoemSettingsFlagMessage";

interface PoemSettingsSectionProps {
    title: string;
    titleValue?: string;
    getSwitchValue: () => boolean;
    switchFunc?: (on: boolean) => void;
    hasChanged: boolean;
    unsuitableToAnalysis: boolean;
    children?: React.ReactElement;
    readonly?: boolean;
}

export default function PoemSettingsSection({ title, titleValue, getSwitchValue, switchFunc, hasChanged, unsuitableToAnalysis, children, readonly } : PoemSettingsSectionProps) {

    const flagMessages: PoemSettingsFlagMessage[] = [
        unsuitableToAnalysis && "unsuitableToAnalysis",
        hasChanged && "changed"
      ].filter(Boolean) as PoemSettingsFlagMessage[];

    return (
        <>
            <div className="w-full flex gap-4 justify-between">
                {
                    <div className="flex flex-col grow">
                        <Title text={title} value={titleValue} />
                        <div className={"min-h-[40px] grid place-items-center"}>
                            { children }
                        </div>
                    </div>
                }
                {
                    switchFunc
                        ? (
                            <>
                                <div className="flex flex-col flex-none gap-2">
                                    <Title text="Náhodně" />
                                    <div className={"flex flex-col justify-center items-center"}>
                                        <Switch
                                            disabled={readonly}
                                            checked={getSwitchValue()}
                                            onCheckedChange={switchFunc}
                                             />
                                    </div>
                                </div>
                            </>
                        )
                        : null
                }
            </div>
            <Flag messages={flagMessages}/>
        </>
    )
}