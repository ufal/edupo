"use client"
import { useEffect } from "react";

import { usePoem } from "@/store/poemStore";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";
import { usePoemGenerator } from "@/hooks/usePoemGenerator";

import apiParams from "@/data/api/params.json";
import apiParamsTitles from "@/data/api/params-titles.json";
import analysisTresholdValues from "@/data/api/analysis-values-tresholds.json";

import Section from "./PoemSettingsSection";
import { Slider } from "../ui/slider";
import { Combobox } from "../ui/combobox";
import { Button } from "../ui/button";
import { ShuffleIcon } from "@radix-ui/react-icons";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

import PoemSettingsChangeBadge from "./PoemSettingsChangeBadge";

export default function PoemSettings() {
  const {
    currentValues,
    setParam,
    disabledFields,
    setDisabledField,
    draftValues,
    setDraftParam,
    hasDraftParamChanged,
    poemLoading
  } = usePoem();
  
  const {
    currentAnalysisValues
  } = usePoemAnalysis.getState();

  const {
    fetchPoem,
    fetchAnalysis,
    fetchMotives
  } = usePoemGenerator();

  const onAnalyseButtonClick = () => {
    if (currentValues.id) {
      fetchAnalysis(currentValues.id);
      fetchMotives(currentValues.id);
    }
  };

  const onGenAnalyseButtonClick = async () => {

    const newPoemId = await fetchPoem();
    await fetchAnalysis(newPoemId);
    await fetchMotives(newPoemId);
  };

  const havePoemLinesChanged = usePoem((s) => s.hasDraftParamChanged("poemLines"));
  const rhymeScheme = draftValues.versesCount === 4 ? apiParams.gen.rhymeScheme["4"] : (draftValues.versesCount === 6 ? apiParams.gen.rhymeScheme["6"] : null);

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

  useEffect(() => {
    const validSchemes = apiParams.gen.rhymeScheme[draftValues.versesCount as 4 | 6] || [];
    setDraftParam("rhymeScheme", validSchemes[0]);
    
  }, [draftValues.versesCount]);

  const heightElements = [
    { value: 64, unit: "px" },
    { value: 64, unit: "px" },
    { value: (!poemLoading && havePoemLinesChanged) ? 66 : 0, unit: "px" },
    { value: (!poemLoading && havePoemLinesChanged) ? 2 : 0, unit: "rem" },
    { value: 40, unit: "px" },
    { value: 8, unit: "px" },
    { value: 64, unit: "px" },
  ];

  const heightStr = `calc(100vh - ${heightElements
    .map((el) => `${el.value}${el.unit}`)
    .join(" - ")})`;

  return (
    <div className="flex flex-col h-full">
        {
            (!poemLoading && havePoemLinesChanged) && <PoemSettingsChangeBadge />
        }
        <div className={"flex-1 overflow-y-auto px-docOffsetXSmall tablet:px-docOffsetXBig pb-4"} style={{ maxHeight: heightStr}}>
            <Accordion type="multiple">
                <AccordionItem value="item-1">
                    <AccordionTrigger>
                        Základní nastavení
                    </AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-2">
                        <Section
                            title="Podle autora"
                            getSwitchValue={() => disabledFields.author}
                            switchFunc={(on) => setDisabledField("author", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("author")}
                            unsuitableToAnalysis={false}
                            readonly={true}>
                            <Combobox
                                placeholder="Podle autora"
                                data={[
                                    { label: "Karel Jaromír Erben", value: "Karel Jaromír Erben" },
                                    { label: "Jaroslav Vrchlický", value: "Jaroslav Vrchlický" }
                                ]}
                                disabled={true || disabledFields.author}
                                value={draftValues.author}
                                onChange={(v) => setDraftParam("author", v)} />
                        </Section>
                        <Section
                            title="Název"
                            getSwitchValue={() => disabledFields.name}
                            switchFunc={(on) => setDisabledField("name", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("name")}
                            unsuitableToAnalysis={false}
                            readonly={true}>
                                <Combobox
                                    placeholder="Název"
                                    data={[
                                        { label: "Polednice", value: "Polednice" },
                                        { label: "Za trochu lásky", value: "Za trochu lásky" }
                                    ]}
                                    disabled={true || disabledFields.name}
                                    value={draftValues.name}
                                    onChange={(v) => setDraftParam("name", v)} />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-2">
                    <AccordionTrigger>
                        Rozšířené nastavení
                    </AccordionTrigger>
                    <AccordionContent className="flex flex-col gap-2">
                        <Section
                            title="Styl"
                            getSwitchValue={() => disabledFields.style}
                            switchFunc={(on) => setDisabledField("style", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("style")}
                            unsuitableToAnalysis={false}
                            readonly={true}>
                                <Combobox
                                    placeholder="Styl"
                                    data={[
                                        { label: "Romantismus", value: "Romantismus" },
                                        { label: "Impresionismus", value: "Impresionismus" }
                                    ]}
                                    disabled={true || disabledFields.style}
                                    value={draftValues.style}
                                    onChange={(v) => setDraftParam("style", v)} />
                        </Section>
                        <Section
                            title="Forma"
                            getSwitchValue={() => disabledFields.form}
                            switchFunc={(on) => setDisabledField("form", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("form")}
                            unsuitableToAnalysis={false}
                            readonly={true}>
                                <Combobox
                                    highlighted={!poemLoading && hasDraftParamChanged("form")}
                                    placeholder="Forma"
                                    data={[
                                        { label: "Volný verš", value: "Volný verš" },
                                        { label: "Sonet", value: "Sonet" },
                                        { label: "Rondel", value: "Rondel" }
                                    ]}
                                    disabled={true || disabledFields.form}
                                    value={draftValues.form}
                                    onChange={(v) => setDraftParam("form", v)} />
                        </Section>
                        <div className="flex flex-row gap-6">
                            <div className="w-1/2 flex flex-col gap-2">
                                <Section
                                    title="Metrum"
                                    getSwitchValue={() => disabledFields.metre}
                                    switchFunc={(on) => setDisabledField("metre", on)}
                                    hasChanged={!poemLoading && hasDraftParamChanged("metre")}
                                    unsuitableToAnalysis={
                                        !disabledFields.metre &&
                                        !!currentAnalysisValues.metreAccuracy &&
                                        (currentAnalysisValues.metreAccuracy < analysisTresholdValues.metreAccuracy)
                                    }>
                                        <Combobox
                                            highlighted={!poemLoading && hasDraftParamChanged("metre")}
                                            placeholder="Metrum"
                                            data={inputParams.metre || []}
                                            disabled={disabledFields.metre}
                                            value={draftValues.metre}
                                            onChange={(v) => setDraftParam("metre", v)} />
                                </Section>
                            </div>
                            <div className="w-1/2 flex flex-col gap-2">
                                <Section
                                    title="Rýmové schéma"
                                    getSwitchValue={() => disabledFields.rhymeScheme}
                                    switchFunc={(on) => setDisabledField("rhymeScheme", on)}
                                    hasChanged={!poemLoading && hasDraftParamChanged("rhymeScheme")}
                                    unsuitableToAnalysis={
                                        !disabledFields.rhymeScheme &&
                                        !!currentAnalysisValues.rhymeSchemeAccuracy &&
                                        (currentAnalysisValues.rhymeSchemeAccuracy < analysisTresholdValues.rhymeSchemeAccuracy)
                                    }>
                                        <Combobox
                                            highlighted={!poemLoading && hasDraftParamChanged("rhymeScheme")}
                                            placeholder="Schéma"
                                            data={inputParams.rhymeScheme || []}
                                            disabled={disabledFields.rhymeScheme}
                                            value={draftValues.rhymeScheme}
                                            onChange={(v) => setDraftParam("rhymeScheme", v)} />
                                </Section>
                            </div>
                        </div>
                        <Section
                            title="Motivy básně"
                            getSwitchValue={() => disabledFields.motives}
                            switchFunc={(on) => setDisabledField("motives", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("motives")}
                            unsuitableToAnalysis={false}
                            readonly={true}>
                                <Textarea
                                    value={draftValues.motives}
                                    className="font-normal"
                                    disabled={disabledFields.motives}
                                    readOnly={true} />
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
                            titleValue={String(draftValues.versesCount)}
                            getSwitchValue={() => disabledFields.versesCount}
                            switchFunc={(on) => setDisabledField("versesCount", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("versesCount")}
                            unsuitableToAnalysis={false}>
                                <Slider
                                    defaultValue={[draftValues.versesCount]}
                                    min={apiParams.gen.versesCount.min}
                                    max={apiParams.gen.versesCount.max}
                                    step={2}
                                    onValueChange={(v) => setDraftParam("versesCount", v[0])}
                                    disabled={disabledFields.versesCount} />
                        </Section>
                        <Section
                            title="Počet slabik v prvním verši"
                            titleValue={String(draftValues.syllablesCount)}
                            getSwitchValue={() => disabledFields.syllablesCount}
                            switchFunc={(on) => setDisabledField("syllablesCount", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("syllablesCount")}
                            unsuitableToAnalysis={false}>
                                <Slider
                                    defaultValue={[draftValues.syllablesCount]}
                                    min={apiParams.gen.syllablesCount.min}
                                    max={apiParams.gen.syllablesCount.max}
                                    step={1}
                                    onValueChange={(v) => setDraftParam("syllablesCount", v[0])}
                                    disabled={disabledFields.syllablesCount} />
                        </Section>
                        <Section
                            title="Temperature"
                            titleValue={String(draftValues.temperature)}
                            switchFunc={(on) => setDisabledField("temperature", on)}
                            getSwitchValue={() => disabledFields.temperature}
                            hasChanged={!poemLoading && hasDraftParamChanged("temperature")}
                            unsuitableToAnalysis={false}>
                                <Slider
                                    defaultValue={[draftValues.temperature]}
                                    min={apiParams.gen.temperature.min}
                                    max={apiParams.gen.temperature.max}
                                    step={0.1}
                                    onValueChange={(v) => setDraftParam("temperature", v[0])}
                                    disabled={disabledFields.temperature} />
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
                disabled={poemLoading && !havePoemLinesChanged}
                variant="outline"
                className="flex-1 bg-slateSoft"
                onClick={onAnalyseButtonClick}>
                    Znovu analyzovat
            </Button>
            <Button
                disabled={poemLoading}
                variant="outline"
                className="flex-1 bg-blueCharcoal text-creamy"
                onClick={onGenAnalyseButtonClick}>
                    Generovat báseň a analyzovat
                    <ShuffleIcon className="ml-1" />
            </Button>
        </div>
    </div>
  )
}