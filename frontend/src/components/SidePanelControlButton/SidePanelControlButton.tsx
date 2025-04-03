"use client"

import { twMerge } from "tailwind-merge";
import { Button } from "@/components/ui/button";

interface SidePanelControlButtonProps {
    filled: boolean;
    onClick: () => void;
}

export default function SidePanelControlButton({ filled, onClick } : SidePanelControlButtonProps) {
    const cls = twMerge(
        "px-6",
        filled ? "bg-white shadow-md" : "bg-transparent text-graySoft border border-graySoft hover:bg-white hover:border-graySoft"
    );

    return (
        <Button variant="outline" className={cls} onClick={onClick}>
            <img src="/svg/panel-right-close.svg" className="w-4 h-4" />
            Generování a analýza
        </Button>
    )
}