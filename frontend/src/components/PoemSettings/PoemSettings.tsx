"use client"
import { usePoemParams } from "@/store/poemSettingsStore";

import apiParams from "@/data/api-params.json";
import defaultApiParams from "@/data/default-api-params.json";

import Section from "./PoemSection";
import { Slider } from "../ui/slider";
import { Combobox } from "../ui/combobox";
import { Button } from "../ui/button";
import { ShuffleIcon } from "@radix-ui/react-icons";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

interface PoemParamsProps {
  analyseButtonClick: () => void;
  genAnalyseButtonClick: () => void;
}

export default function PoemParams({ analyseButtonClick, genAnalyseButtonClick }: PoemParamsProps) {
  const {
    temperature,
    syllablesCount,
    versesCount,
    disabledFields,
    setTemperature,
    setSyllablesCount,
    setVersesCount,
    setDisabledField,
  } = usePoemParams();

  return (
    <div className="w-full h-full flex-1 flex flex-col font-bold justify-end">

        <div className="flex-1 px-docOffsetXSmall tablet:px-docOffsetXBig pb-4">
            <Accordion type="multiple">
                <AccordionItem value="item-1">
                    <AccordionTrigger>
                        Základní nastavení
                    </AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-4">
                        <Section
                            title="Podle autora"
                            switchFunc={(on) => setDisabledField("author", on)}>
                            <Combobox
                                placeholder="Podle autora"
                                data={[
                                    { label: "Karel Jaromír Erben", value: "Karel Jaromír Erben" },
                                    { label: "Jaroslav Vrchlický", value: "Jaroslav Vrchlický" }
                                ]}
                                disabled={disabledFields.author} />
                        </Section>
                        <Section
                            title="Název"
                            switchFunc={(on) => setDisabledField("name", on)}>
                                <Combobox
                                    placeholder="Název"
                                    data={[
                                        { label: "Polednice", value: "Polednice" },
                                        { label: "Za trochu lásky", value: "Za trochu lásky" }
                                    ]}
                                    disabled={disabledFields.name} />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                    <AccordionTrigger>
                        Rozšířené nastavení
                    </AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-4">
                    <Section
                            title="Styl"
                            switchFunc={(on) => setDisabledField("style", on)}>
                                <Combobox
                                    placeholder="Styl"
                                    data={[
                                        { label: "Romantismus", value: "Romantismus" },
                                        { label: "Impresionismus", value: "Impresionismus" }
                                    ]}
                                    disabled={disabledFields.style} />
                        </Section>
                        <Section
                            title="Forma"
                            switchFunc={(on) => setDisabledField("form", on)}>
                                <Combobox
                                    placeholder="Forma"
                                    data={[
                                        { label: "Volný verš", value: "Volný verš" },
                                        { label: "Sonet", value: "Sonet" },
                                        { label: "Rondel", value: "Rondel" }
                                    ]}
                                    disabled={disabledFields.form} />
                        </Section>
                        <div className="flex flex-row gap-6">
                            <div className="w-1/2">
                                <Section
                                    title="Metrum"
                                    switchFunc={(on) => setDisabledField("metrum", on)}>
                                        <Combobox
                                            placeholder="Metrum"
                                            data={[
                                                { label: "Jamb", value: "Jamb" },
                                                { label: "Trochej", value: "Trochej" },
                                                { label: "Daktyl", value: "Daktyl" }
                                            ]}
                                            disabled={disabledFields.metrum} />
                                </Section>
                            </div>
                            <div className="w-1/2">
                                <Section
                                    title="Rýmové schéma"
                                    switchFunc={(on) => setDisabledField("rhyme", on)}>
                                        <Combobox
                                            placeholder="Schéma"
                                            data={[
                                                { label: "ABABCC", value: "ABABCC" },
                                                { label: "ABBABA", value: "ABBABA" }
                                            ]}
                                            disabled={disabledFields.rhyme} />
                                </Section>
                            </div>
                        </div>
                        <Section
                            title="Motivy básně"
                            switchFunc={(on) => setDisabledField("motives", on)}>
                                <Textarea
                                    className="font-normal"
                                    placeholder="Napište motivy nebo slova veršů"
                                    disabled={disabledFields.motives}
                                    />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                    <AccordionTrigger>
                        Nastavení generování
                    </AccordionTrigger>
                    <AccordionContent>
                        <Section
                            title="Počet veršů"
                            titleValue={String(versesCount)}
                            switchFunc={(on) => setDisabledField("versesCount", on)}>
                                <Slider
                                    defaultValue={[defaultApiParams.gen.versesCount]}
                                    min={apiParams.gen.versesCount.min}
                                    max={apiParams.gen.versesCount.max}
                                    step={1}
                                    onValueChange={(v) => setVersesCount(v[0])}
                                    disabled={disabledFields.versesCount}
                                />
                        </Section>
                        <Section
                            title="Počet slabik v prvním verši"
                            titleValue={String(syllablesCount)}
                            switchFunc={(on) => setDisabledField("syllablesCount", on)}>
                                <Slider
                                    defaultValue={[defaultApiParams.gen.syllablesCount]}
                                    min={apiParams.gen.syllablesCount.min}
                                    max={apiParams.gen.syllablesCount.max}
                                    step={1}
                                    onValueChange={(v) => setSyllablesCount(v[0])}
                                    disabled={disabledFields.syllablesCount}
                                />
                        </Section>
                        <Section
                            title="Temperature"
                            titleValue={String(temperature)}
                            switchFunc={(on) => setDisabledField("temperature", on)}>
                                <Slider
                                    defaultValue={[defaultApiParams.gen.temperature]}
                                    min={apiParams.gen.temperature.min}
                                    max={apiParams.gen.temperature.max}
                                    step={0.1}
                                    onValueChange={(v) => setTemperature(v[0])}
                                    disabled={disabledFields.temperature}
                                />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </div>
        <div className="w-full h-[64px] flex flex-row items-center px-docOffsetXSmall tablet:px-docOffsetXBig gap-4 inset-shadow-sm">
            <Button variant="outline" className="flex-1 bg-slateSoft" onClick={analyseButtonClick}>
                Znovu analyzovat
            </Button>
            <Button variant="outline" className="flex-1 bg-blueCharcoal text-creamy" onClick={genAnalyseButtonClick}>
                Generovat báseň a analyzovat
                <ShuffleIcon className="ml-1" />
            </Button>
        </div>
    </div>
  )
}