"use client"

import * as React from "react";
import { cn } from "@/lib/utils"
import Link from "next/link";

import { crimsonPro } from "@/app/(webapp)/fonts";

import { Button } from "@/components/ui/button";
import { Link as LinkIcon, QrCode, Check, ChevronsUpDown } from "lucide-react";
import { Command, CommandEmpty, CommandGroup, CommandItem, CommandList } from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";

import { usePoem } from "@/store/poemStore";
import { usePoemLoader } from "@/hooks/useLoadPoem";
import { AnalysisResponse } from "@/types/edupoApi";
import { usePoemDatabase } from "@/store/poemDatabaseStore";

import presetPoems from "@/data/api/preset-poems.json"

export default function Header() {
    const {
        setDraftParam
    } = usePoem.getState();

    const { loadPoem } = usePoemLoader();

    const [open, setOpen] = React.useState(false);
    const [value, setValue] = React.useState("");

    return (
        <header className="w-full h-16 bg-crimsonRed flex gap-6 justify-between items-center flex-wrap px-docOffsetXSmall tablet:px-docOffsetXBig py-docOffsetY text-white">

            <div className="flex flex-row items-center gap-3">
                <Link href={process.env.NEXT_PUBLIC_LINK_BASE || "/"}>
                    <div className={crimsonPro.className + " pr-3 text-3xl font-bold border-r-2 border-white"}>
                        EduPo
                    </div>
                </Link>
    
                <Link href="https://cuni.cz" target="_blank">
                    <img src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "svg/logo-uk.svg"} alt="Logo UK" className="w-8 h-8" />
                </Link>
                
                <Link href="https://ucl.cas.cz/" target="_blank">
                    <img src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "svg/logo-ucl.svg"} alt="Logo ÚČL AV ČR" className="w-8 h-8" />
                </Link>
            </div>

            <Popover open={open} onOpenChange={setOpen}>
                <PopoverTrigger asChild>
                    <Button
                        variant="outline"
                        role="combobox"
                        aria-expanded={open}
                        className="w-[340px] justify-between text-black overflow-hidden">
                        {
                            value
                                ? value
                                : "Načti předpřipravenou ukázku"
                        }
                        <ChevronsUpDown className="opacity-50" />
                    </Button>
                </PopoverTrigger>
                <PopoverContent className="w-[340px] p-0">
                    <Command>
                        <CommandList>
                            <CommandEmpty>Nic nenalezeno.</CommandEmpty>
                            <CommandGroup>
                            {
                                presetPoems.map(poem => {
                                    const entry = poem.author + ": " + poem.poem;

                                    return (
                                        <CommandItem
                                            key={entry}
                                            value={entry}
                                            onSelect={(currentValue) => {
                                                setValue(currentValue === value ? "" : currentValue);
                                                setOpen(false);

                                                try {
                                                    const currentValueId = presetPoems.find(e => (e.author + ": " + e.poem) === currentValue)?.id!
                                                    loadPoem(currentValueId.toString(), async (data: AnalysisResponse) => {
                                                        
                                                        if (data.author)
                                                            setDraftParam("author", data.author);
                                                        await usePoemDatabase.getState().fetchPoemsForAuthor(data.author);

                                                        const poemTitle = presetPoems.find(e => e.id === currentValueId)?.poem;

                                                        if (poemTitle) {
                                                            setDraftParam("title", poemTitle);
                                                        }
                                                    });
                                                } catch (err: any) {
                                                    console.error("Error fetching poem:", err);
                                                }
                                            }}>
                                                { entry }
                                                <Check
                                                    className={
                                                        cn(
                                                            "ml-auto",
                                                            value === entry ? "opacity-100" : "opacity-0"
                                                        )
                                                    }
                                                />
                                        </CommandItem>
                                    )
                                })
                            }
                            </CommandGroup>
                        </CommandList>
                    </Command>
                </PopoverContent>
            </Popover>

            <div className="flex gap-2">
                <Button variant="outline" size="icon" className="text-black">
                    <LinkIcon />
                </Button>
                <Button variant="outline" size="icon" className="text-black">
                    <QrCode />
                </Button>
            </div>
            
        </header>
    )
}
