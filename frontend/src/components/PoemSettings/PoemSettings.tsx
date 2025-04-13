import Section from "./PoemSection";
import { Slider } from "../ui/slider";
import { Combobox } from "../ui/combobox";
import { Button } from "../ui/button";
import { ShuffleIcon } from "@radix-ui/react-icons";
import { Textarea } from "@/components/ui/textarea";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

export default function PoemParams() {
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
                            withSwitch={true}>
                            <Combobox
                                placeholder="Podle autora"
                                data={[
                                    { label: "Karel Jaromír Erben", value: "Karel Jaromír Erben" },
                                    { label: "Jaroslav Vrchlický", value: "Jaroslav Vrchlický" }
                                ]} />
                        </Section>
                        <Section
                            title="Název"
                            withSwitch={true}>
                                <Combobox
                                    placeholder="Název"
                                    data={[
                                        { label: "Polednice", value: "Polednice" },
                                        { label: "Za trochu lásky", value: "Za trochu lásky" }
                                    ]} />
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
                            withSwitch={true}>
                                <Combobox
                                    placeholder="Styl"
                                    data={[
                                        { label: "Romantismus", value: "Romantismus" },
                                        { label: "Impresionismus", value: "Impresionismus" }
                                    ]} />
                        </Section>
                        <Section
                            title="Forma"
                            withSwitch={true}>
                                <Combobox
                                    placeholder="Forma"
                                    data={[
                                        { label: "Volný verš", value: "Volný verš" },
                                        { label: "Sonet", value: "Sonet" },
                                        { label: "Rondel", value: "Rondel" }
                                    ]} />
                        </Section>
                        <div className="flex flex-row gap-6">
                            <div className="w-1/2">
                                <Section
                                    title="Metrum"
                                    withSwitch={true}>
                                        <Combobox
                                            placeholder="Metrum"
                                            data={[
                                                { label: "Jamb", value: "Jamb" },
                                                { label: "Trochej", value: "Trochej" },
                                                { label: "Daktyl", value: "Daktyl" }
                                            ]} />
                                </Section>
                            </div>
                            <div className="w-1/2">
                                <Section
                                    title="Rýmové schéma"
                                    withSwitch={true}>
                                        <Combobox
                                            placeholder="Schéma"
                                            data={[
                                                { label: "ABABCC", value: "ABABCC" },
                                                { label: "ABBABA", value: "ABBABA" }
                                            ]} />
                                </Section>
                            </div>
                        </div>
                        <Section
                            title="Motivy básně"
                            withSwitch={true}>
                                <Textarea
                                    className="font-normal"
                                    placeholder="Napište motivy nebo slova veršů"
                                    />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
                <AccordionItem value="item-3">
                    <AccordionTrigger>
                        Nastavení generování
                    </AccordionTrigger>
                    <AccordionContent>
                        <Section title="Počet veršů" withSwitch={true}>
                            <Slider defaultValue={[5]} min={2} max={6} step={1} />
                        </Section>
                        <Section title="Počet slabik v prvním verši" withSwitch={true}>
                            <Slider defaultValue={[4]} min={4} max={10} step={1} />
                        </Section>
                        <Section title="Temperature" withSwitch={true}>
                            <Slider defaultValue={[0.56]} max={1} step={0.05} />
                        </Section>
                    </AccordionContent>
                </AccordionItem>
            </Accordion>
        </div>
        <div className="w-full h-[64px] flex flex-row items-center px-docOffsetXSmall tablet:px-docOffsetXBig gap-4 inset-shadow-sm">
            <Button variant="outline" className="flex-1 bg-slateSoft">
                Znovu analyzovat
            </Button>
            <Button variant="outline" className="flex-1 bg-blueCharcoal text-creamy">
                Generovat báseň a analyzovat
                <ShuffleIcon className="ml-1" />
            </Button>
        </div>

        {
            /*
        <Collapsible>
            <CollapsibleTrigger>Základní</CollapsibleTrigger>
            <CollapsibleContent>
                <Section withSwitch={true}>
                    <div className="flex flex-col grow justify-between">
                        {"Temperature"}
                        <div className="flex h-[24px]">
                            <Slider defaultValue={[0.56]} max={1} step={0.05} />
                        </div>
                    </div>
                </Section>
            </CollapsibleContent>
        </Collapsible>
        <Collapsible>
            <CollapsibleTrigger>Pokročilé</CollapsibleTrigger>
            <CollapsibleContent>
                <Section withSwitch={true}>
                    <div className="flex flex-col grow justify-between">
                        {"Temperature"}
                        <div className="flex h-[24px]">
                            <Slider defaultValue={[0.56]} max={1} step={0.05} />
                        </div>
                    </div>
                </Section>
            </CollapsibleContent>
        </Collapsible>
            */
        }

    </div>
  )
}