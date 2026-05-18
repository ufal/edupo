import { usePoem } from "@/store/poemStore";
import { twMerge } from "tailwind-merge";
import { useState, useEffect } from "react";
import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";

export default function PoemPlayBadge({ cls }: { cls: string }) {
    const poemId = usePoem((s) => s.currentValues.id);
    const poemLoading = usePoem((s) => s.poemLoading);

    const { fetchTTS } = usePoemGenerator();
    const { toggle, isPlaying, stop } = useAudioPlayer();

    const [isFetchingTTS, setIsFetchingTTS] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);

    useEffect(() => {
        setAudioUrl(null);
        stop();
    }, [poemId, stop]);

    const onClick = async () => {
      if (!poemId) return;

      try {
        if (audioUrl) {
          toggle(audioUrl);
          return;
        }

        console.log("Fetching TTS... ", poemId);
        setIsFetchingTTS(true);

        const ttsResp = await fetchTTS(poemId);

        if (ttsResp.url) {
          setAudioUrl(ttsResp.url);
          toggle(ttsResp.url);
        }

      } catch (err) {
        console.error("Error fetching TTS:", err);
      } finally {
        setIsFetchingTTS(false);
      }
    };

    const customCls = twMerge(cls, poemLoading ? "opacity-50" : "cursor-pointer");
    const onClickHandler = poemLoading ? undefined : onClick;

    return (
        <div
            className={twMerge("relative flex justify-center items-center w-[36px] h-[36px] rounded-full bg-slate200 border-1 border-solid border-slate400", customCls)}
            onClick={onClickHandler}>

                {isFetchingTTS && (
                    <div className="absolute inset-0 flex items-center justify-center bg-white/70 rounded-full text-xs text-gray-500">
                        ⏳
                    </div>
                )}

                {!isFetchingTTS && (
                    <img
                        src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + (isPlaying ? "svg/pause.svg" : "svg/play.svg")}
                        className="w-[16px] h-[16px]"
                        alt={isPlaying ? "Pause" : "Play"}
                    />
                )}

        </div>
    )
}