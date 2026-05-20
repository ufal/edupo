import PoemSettings from "../Modes/PoemSettings/PoemSettings";
import ImageGen from "../Modes/ImageGen";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export type PoemSettingsMode = "poem" | "image";

export default function PoemSettingsModeSwitcher({ defaultMode }: { defaultMode?: PoemSettingsMode }) {
  return (
      <Tabs defaultValue={defaultMode} className="w-full h-full flex flex-col">
        <h2 className="pt-[24px] pb-[16px] px-docOffsetXSmall tablet:px-docOffsetXBig">
          Generování a analýza básně
        </h2>
        <div className="px-docOffsetXSmall tablet:px-docOffsetXBig">
          <TabsList className="w-full bg-silverTransparent">
            <TabsTrigger value="poem" className="w-1/2">Báseň</TabsTrigger>
            <TabsTrigger value="image" className="w-1/2">Obrázek</TabsTrigger>
          </TabsList>
        </div>
        <TabsContent value="poem" className="flex-1">
          <PoemSettings />
        </TabsContent>
        <TabsContent value="image">
          <ImageGen />
        </TabsContent>
      </Tabs>
  )
}