"use client"
import { usePoemParams } from "@/store/poemSettingsStore";

import apiParams from "@/data/api/params.json";
import defaultApiParams from "@/data/api/params-default-values.json";
import apiParamsTitles from "@/data/api/params-titles.json";

import Section from "./PoemSection";
import { Slider } from "../ui/slider";
import { Combobox } from "../ui/combobox";
import { Button } from "../ui/button";
import { ShuffleIcon } from "@radix-ui/react-icons";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { twMerge } from "tailwind-merge";

interface PoemParamsProps {
  analyseButtonClick: () => void;
  genAnalyseButtonClick: () => void;
}

export default function PoemParams({ analyseButtonClick, genAnalyseButtonClick }: PoemParamsProps) {
  const {
    disabledFields,
    setDisabledField,
    currentValues,
    hasParamChanged
  } = usePoemParams();

  const setParam = usePoemParams((s) => s.setParam);
  const havePoemLinesChanged = usePoemParams((s) => s.hasParamChanged("poemLines"));
  // const haveParamsChanged = usePoemParams((s) => s.haveParamsChanged());

  const rhymeScheme = currentValues.versesCount === 4 ? apiParams.gen.rhymeScheme["4"] : (currentValues.versesCount === 6 ? apiParams.gen.rhymeScheme["6"] : null);

  type MeterCode = keyof typeof apiParamsTitles.gen.metre;

  const inputParams = {
    metre: apiParams.gen.metre.map((i) => ({
      label: apiParamsTitles.gen.metre[i as MeterCode] ?? i,
      value: i
    })),
    rhymeScheme: rhymeScheme?.map((i) => ({
      label: i,
      value: i
    }))
  }

  return (
    <div className="flex flex-col h-full"> 
        <div className={"flex-1 overflow-y-auto px-docOffsetXSmall tablet:px-docOffsetXBig pb-4"} style={{ maxHeight: "calc(100vh - 64px - 64px - 40px - 8px - 64px)"}}>
            <Accordion type="multiple">
                <AccordionItem value="item-1">
                    <AccordionTrigger>
                        Základní nastavení
                    </AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-4">
                        <Section
                            title="Podle autora"
                            switchFunc={(on) => setDisabledField("author", on)}
                            hasChanged={hasParamChanged("author")}>
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
                            switchFunc={(on) => setDisabledField("name", on)}
                            hasChanged={hasParamChanged("name")}>
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
                            switchFunc={(on) => setDisabledField("style", on)}
                            hasChanged={hasParamChanged("style")}>
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
                            switchFunc={(on) => setDisabledField("form", on)}
                            hasChanged={hasParamChanged("form")}>
                                <Combobox
                                    highlighted={hasParamChanged("form")}
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
                                    switchFunc={(on) => setDisabledField("metre", on)}
                                    hasChanged={hasParamChanged("metre")}>
                                        <Combobox
                                            highlighted={hasParamChanged("metre")}
                                            placeholder="Metrum"
                                            data={inputParams.metre || []}
                                            disabled={disabledFields.metre} />
                                </Section>
                            </div>
                            <div className="w-1/2">
                                <Section
                                    title="Rýmové schéma"
                                    switchFunc={(on) => setDisabledField("rhymeScheme", on)}
                                    hasChanged={hasParamChanged("rhymeScheme")}>
                                        <Combobox
                                            highlighted={hasParamChanged("rhymeScheme")}
                                            placeholder="Schéma"
                                            data={inputParams.rhymeScheme || []}
                                            disabled={disabledFields.rhymeScheme} />
                                </Section>
                            </div>
                        </div>
                        <Section
                            title="Motivy básně"
                            switchFunc={(on) => setDisabledField("motives", on)}
                            hasChanged={hasParamChanged("motives")}>
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
                            titleValue={String(currentValues.versesCount)}
                            switchFunc={(on) => setDisabledField("versesCount", on)}
                            hasChanged={hasParamChanged("versesCount")}>
                                <Slider
                                    defaultValue={[defaultApiParams.gen.versesCount]}
                                    min={apiParams.gen.versesCount.min}
                                    max={apiParams.gen.versesCount.max}
                                    step={2}
                                    onValueChange={(v) => setParam("versesCount", v[0])}
                                    disabled={disabledFields.versesCount}
                                />
                        </Section>
                        <Section
                            title="Počet slabik v prvním verši"
                            titleValue={String(currentValues.syllablesCount)}
                            switchFunc={(on) => setDisabledField("syllablesCount", on)}
                            hasChanged={hasParamChanged("syllablesCount")}>
                                <Slider
                                    defaultValue={[defaultApiParams.gen.syllablesCount]}
                                    min={apiParams.gen.syllablesCount.min}
                                    max={apiParams.gen.syllablesCount.max}
                                    step={1}
                                    onValueChange={(v) => setParam("syllablesCount", v[0])}
                                    disabled={disabledFields.syllablesCount}
                                />
                        </Section>
                        <Section
                            title="Temperature"
                            titleValue={String(currentValues.temperature)}
                            switchFunc={(on) => setDisabledField("temperature", on)}
                            hasChanged={hasParamChanged("temperature")}
                            >
                                <Slider
                                    defaultValue={[defaultApiParams.gen.temperature]}
                                    min={apiParams.gen.temperature.min}
                                    max={apiParams.gen.temperature.max}
                                    step={0.1}
                                    onValueChange={(v) => setParam("temperature", v[0])}
                                    disabled={disabledFields.temperature}
                                />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </div>
        <div
            className="relative h-[64px] flex flex-row items-center px-docOffsetXSmall tablet:px-docOffsetXBig gap-4 shrink-0"
            style={{
                boxShadow: "0px -3px 6px -2px var(--black-shadow)"
            }}
            >
            <Button
                disabled={!havePoemLinesChanged}
                variant="outline"
                className="flex-1 bg-slateSoft"
                onClick={analyseButtonClick}>
                    Znovu analyzovat
            </Button>
            <Button
                variant="outline"
                className="flex-1 bg-blueCharcoal text-creamy"
                onClick={genAnalyseButtonClick}>
                    Generovat báseň a analyzovat
                    <ShuffleIcon className="ml-1" />
            </Button>
        </div>
    </div>
  )
}