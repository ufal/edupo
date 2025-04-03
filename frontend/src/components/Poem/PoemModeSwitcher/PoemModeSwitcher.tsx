import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface PoemModeSwitcherProps {
  readingModeContent: React.ReactNode;
  analysisModeContent: React.ReactNode;
  editingModeContent: React.ReactNode;
}

function LikeButton() {
  return (
    <Button variant="outline" className="px-6 shadow-sm bg-white">
      <img src="/svg/like.svg" className="w-6 h-6" />
      Líbí se mi
    </Button>
  );
}

export default function PoemModeSwitcher({ readingModeContent, analysisModeContent, editingModeContent }: PoemModeSwitcherProps) {
  return (
    <div className="pt-4 flex-1">
      <Tabs defaultValue="reading" className="w-full h-full flex flex-col">
        <div className="flex flex-row justify-between pr-6">
          <TabsList className="w-[400px] bg-silverTransparent">
            <TabsTrigger value="reading" className="w-1/3">Četba</TabsTrigger>
            <TabsTrigger value="analysis" className="w-1/3">Analýza</TabsTrigger>
            <TabsTrigger value="editing" className="w-1/3">Úpravy textu</TabsTrigger>
          </TabsList>
          <LikeButton />
        </div>
        <TabsContent value="reading" className="flex-1">
            {readingModeContent}
        </TabsContent>
        <TabsContent value="analysis" className="flex-1">
            {analysisModeContent}
        </TabsContent>
        <TabsContent value="editing" className="flex-1">
            {editingModeContent}
        </TabsContent>
      </Tabs>
    </div>
  )
}