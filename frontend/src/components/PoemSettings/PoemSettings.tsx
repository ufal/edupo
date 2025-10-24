"use client"
import { useRouter } from "next/navigation";

import { usePoem } from "@/store/poemStore";
import { usePoemAnalysis } from "@/store/poemAnalysisStore";
import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { usePoemDatabase } from "@/store/poemDatabaseStore";

import apiParams from "@/data/api/params.json";
import apiParamsTitles from "@/data/api/params-titles.json";
import analysisTresholdValues from "@/data/api/analysis-values-tresholds.json";

import Section from "./PoemSettingsSection";
import Title from "./PoemSettingsSection/PoemSettingsTitle";
import { Slider } from "../ui/slider";
import { Combobox } from "../ui/combobox";
import { Button } from "../ui/button";
import { ShuffleIcon } from "@radix-ui/react-icons";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

import PoemSettingsChangeBadge from "./PoemSettingsChangeBadge";
import { Input } from "../ui/input";

export default function PoemSettings() {

  const router = useRouter();

  const {
    currentValues,
    disabledFields,
    setDisabledField,
    draftValues,
    setDraftParam,
    hasDraftParamChanged,
    poemLoading
  } = usePoem();
  
  const {
    currentAnalysisValues,
    analysisLoading
  } = usePoemAnalysis.getState();

  const {
    authors,
    poemsByAuthor
  } = usePoemDatabase();

  const {
    genPoem,
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
    setDraftParam("motives", "");
    const newPoemId = await genPoem();

    if (newPoemId) {
        await fetchAnalysis(newPoemId);
        await fetchMotives(newPoemId);

        const currentPath = window.location.pathname;
        router.replace(`${currentPath}?poemId=${newPoemId}`);
    }
  };

  const havePoemLinesChanged = usePoem((s) => s.hasDraftParamChanged("poemLines"));

  // const rhymeScheme = draftValues.versesCount === 4 ? apiParams.gen.rhymeScheme["4"] : (draftValues.versesCount === 6 ? apiParams.gen.rhymeScheme["6"] : null);

  type MeterCode = keyof typeof apiParamsTitles.gen.metre;

  const inputParams = {
    metre: apiParams.gen.metre.map((i) => ({
        label: apiParamsTitles.gen.metre[i as MeterCode] ?? i,
        value: i
    })),
    form: apiParams.gen.form.map((i) => ({
        label: i,
        value: i.charAt(0).toUpperCase() + i.slice(1)
    }))
  }

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

  const authorOptions = authors.map(a => ({ label: a, value: a }));

  const validAuthor = authorOptions.some(item => item.value === draftValues.author)
    ? draftValues.author
    : "";

  const poemOptions = draftValues.author && poemsByAuthor[draftValues.author]
    ? poemsByAuthor[draftValues.author].map(p => ({ label: p.title, value: p.title }))
    : [];

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
                            switchFunc={(on) => {
                                setDisabledField("author", on);

                                if (on && !disabledFields.title)
                                    setDisabledField("title", on);
                            }}
                            hasChanged={!poemLoading && (hasDraftParamChanged("author") && draftValues.author !== "")}
                            unsuitableToAnalysis={false}>
                            <Combobox
                                withSearch={true}
                                placeholder="Podle autora"
                                data={authorOptions}
                                disabled={disabledFields.author}
                                value={validAuthor}
                                onChange={(v) => {
                                    setDraftParam("author", v);
                                    setDraftParam("title", "");
                                    usePoemDatabase.getState().fetchPoemsForAuthor(v);
                                }}
                            />
                        </Section>
                        <Section
                            title="Název"
                            getSwitchValue={() => disabledFields.title}
                            switchFunc={(on) => setDisabledField("title", on)}
                            hasChanged={!poemLoading && (hasDraftParamChanged("title") && draftValues.title !== "")}
                            unsuitableToAnalysis={false}>
                            <Combobox
                                withSearch
                                allowCustomInput
                                placeholder="Název"
                                data={poemOptions}
                                disabled={
                                    false
                                    /*
                                    disabledFields.author ||
                                    disabledFields.title ||
                                    !draftValues.author ||
                                    !(draftValues.author in poemsByAuthor)
                                    */
                                }
                                value={draftValues.title}
                                onChange={(v) => setDraftParam("title", v)}
                            />
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
                            unsuitableToAnalysis={false}>
                                <Combobox
                                    highlighted={!poemLoading && hasDraftParamChanged("form")}
                                    placeholder="Forma"
                                    data={inputParams.form || []}
                                    disabled={disabledFields.form}
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
                                        draftValues.metre !== "" &&
                                        currentAnalysisValues.metre != null &&
                                        (!analysisLoading && !poemLoading && !hasDraftParamChanged("metre")) &&
                                        (currentAnalysisValues.metre !== draftValues.metre)
                                        /*
                                        !disabledFields.metre &&
                                        !!currentAnalysisValues.metreAccuracy &&
                                        (currentAnalysisValues.metreAccuracy < analysisTresholdValues.metreAccuracy)
                                        */
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
                                    }
                                    readonly={true}>
                                        { /*
                                        <Combobox
                                            highlighted={!poemLoading && hasDraftParamChanged("rhymeScheme")}
                                            placeholder="Schéma"
                                            data={inputParams.rhymeScheme || []}
                                            disabled={disabledFields.rhymeScheme}
                                            value={
                                                draftValues.rhymeScheme
                                                    ? draftValues.rhymeScheme
                                                    : inputParams.rhymeScheme![inputParams.rhymeScheme?.length! - 1].value
                                            }
                                            onChange={(v) => setDraftParam("rhymeScheme", v)} />
                                        */ }
                                        <Input
                                            type="text"
                                            className="focus-visible:ring-0"
                                            value={currentAnalysisValues.rhymeScheme ?? ""}
                                            disabled={true} />
                                </Section>
                            </div>
                        </div>
                        {
                            /*
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
                            */
                        }

                        <div>
                            <Title text={"Motivy"} />
                            <Textarea
                                value={draftValues.motives}
                                className="font-normal"
                                readOnly={true} />
                        </div>
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
                                step={1}
                                onValueChange={(v) => {
                                    const newVersesCount = v[0];
                                    setDraftParam("versesCount", newVersesCount);
                                }}
                                disabled={disabledFields.versesCount} />
                        </Section>
                        <Section
                            title="Počet strof"
                            titleValue={String(draftValues.maxStrophes)}
                            getSwitchValue={() => disabledFields.maxStrophes}
                            switchFunc={(on) => setDisabledField("maxStrophes", on)}
                            hasChanged={!poemLoading && hasDraftParamChanged("maxStrophes")}
                            unsuitableToAnalysis={false}>
                                <Slider
                                    defaultValue={[draftValues.maxStrophes]}
                                    min={apiParams.gen.maxStrophes.min}
                                    max={apiParams.gen.maxStrophes.max}
                                    step={1}
                                    onValueChange={(v) => setDraftParam("maxStrophes", v[0])}
                                    disabled={disabledFields.maxStrophes} />
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