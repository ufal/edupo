import * as React from "react"

import { Switch } from "../../ui/switch";
import Title from "../PoemTitle";

import { Pencil2Icon } from "@radix-ui/react-icons";

interface PoemSectionProps {
    title: string;
    titleValue?: string;
    switchFunc?: (on: boolean) => void;
    hasChanged: boolean;
    children?: React.ReactElement;
}

const inputChangeBadge = (
    <div className="flex flex-cols gap-2 items-center text-blueSky font-light text-sm pb-3">
        <Pencil2Icon className="w-4 h-4 text-blueSky" />
        Parametr byl změněn.
    </div>
);

export default function PoemSection({ title, titleValue, switchFunc, hasChanged, children } : PoemSectionProps) {
    return (
        <div className="w-full flex gap-4 justify-between">
            {
                <div className="flex flex-col grow">
                    <Title text={title} value={titleValue} />
                    <div className={"min-h-[40px] grid place-items-center"}>
                        { children }
                    </div>
                    { hasChanged && inputChangeBadge }
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