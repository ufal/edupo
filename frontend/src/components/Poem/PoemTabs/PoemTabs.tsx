import LikeButton from "./PoemLikeButton/PoemLikeButton";
import PoemView from "../PoemView";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function PoemTabs() {
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
            <PoemView linesMode="plaintext" />
        </TabsContent>
        <TabsContent value="analysis" className="flex-1">
            <PoemView linesMode="highlighted" />
        </TabsContent>
        <TabsContent value="editing" className="flex-1">
            <PoemView linesMode="editable" />
        </TabsContent>
      </Tabs>
    </div>
  )
}