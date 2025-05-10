import * as React from "react";
import { Pencil2Icon } from "@radix-ui/react-icons";
import { BotIcon } from "lucide-react";
import { PoemSettingsFlagMessage } from "./PoemSettingsFlagMessage";

interface PoemSettingsFlagProps {
    messages: PoemSettingsFlagMessage[];
}

function flagSegment(message: PoemSettingsFlagMessage) {
    const cls = "inline w-4 h-4 text-blueSky";

    switch (message) {
        case "changed":
            return (
                <>
                    <Pencil2Icon className={cls} />
                    Parametr byl změněn
                </>
            );
        case "unsuitableToAnalysis":
            return (
                <>
                    <BotIcon className={cls} />
                    Nepovedlo se dodržet
                </>
            );
        default:
            return null;
    }
}

const placeholderElement = (
    <span className="invisible">
        <Pencil2Icon className="inline w-4 h-4 mr-1" />
        Placeholder text
    </span>
);

export default function PoemSettingsFlag({ messages }: PoemSettingsFlagProps) {
    const renderedMessages = messages
        .map((message, index) => (
            <span key={index} className="flex items-center gap-1">
                {flagSegment(message)}
            </span>
        ))
        .reduce<React.ReactNode[]>((acc, curr, i) => {
            if (i > 0) acc.push(<span key={`sep-${i}`} className="text-blueSky">,</span>);
            acc.push(curr);
            return acc;
        }, []);

    return (
        <div className="min-h-[24px] flex flex-wrap items-center gap-1 text-blueSky font-light text-sm pb-2">
            {messages.length > 0 ? renderedMessages : placeholderElement}
        </div>
    );
}