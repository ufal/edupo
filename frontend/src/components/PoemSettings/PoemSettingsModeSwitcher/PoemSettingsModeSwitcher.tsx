import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface PoemSettingsModeSwitcherProps {
  poemModeContent: React.ReactNode;
  imageModeContent: React.ReactNode;
}

export default function PoemSettingsModeSwitcher({ poemModeContent, imageModeContent }: PoemSettingsModeSwitcherProps) {
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
          {poemModeContent}
        </TabsContent>
        <TabsContent value="image">
          {imageModeContent}
        </TabsContent>
      </Tabs>
  )
}