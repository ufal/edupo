import * as React from "react"

import { Switch } from "../../ui/switch";
import Title from "../PoemTitle";

interface PoemSectionProps {
    title: string;
    titleValue?: string;
    switchFunc?: (on: boolean) => void;
    children?: React.ReactElement;
}

export default function PoemSection({ title, titleValue, switchFunc, children } : PoemSectionProps) {
    return (
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
                                    <Switch onCheckedChange={switchFunc} />
                                </div>
                            </div>
                        </>
                    )
                    : null
            }
        </div>
    )
}