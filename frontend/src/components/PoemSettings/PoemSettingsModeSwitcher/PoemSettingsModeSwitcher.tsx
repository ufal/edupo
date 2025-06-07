import PoemSettings from "../PoemSettings";
import ImageSettings from "../../ImageSettings";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function PoemSettingsModeSwitcher() {
  return (
      <Tabs defaultValue="poem" className="w-full h-full flex flex-col">
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
          <ImageSettings />
        </TabsContent>
      </Tabs>
  )
}