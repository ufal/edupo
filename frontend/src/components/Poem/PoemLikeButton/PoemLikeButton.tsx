import { usePoem } from "@/store/poemStore";
import { Button } from "@/components/ui/button";
import { sendLikeApi } from "@/lib/api/poemApi";
import { useState, useMemo } from "react";

export default function LikeButton() {

  const poemId = usePoem((s) => s.currentValues.id);
  const poemLoading = usePoem((s) => s.poemLoading);
  const [alreadyLikedPoemIds, setAlreadyLikedPoemIds] = useState<Set<string>>(new Set());

  const alreadyLiked = useMemo(() => {
    return poemId ? alreadyLikedPoemIds.has(poemId) : false;
  }, [poemId, alreadyLikedPoemIds]);

  const onClick = async () => {
    if (!poemId) return;

    try {
      const res = await sendLikeApi(poemId);

      if (res && Number.isInteger(res))
        setAlreadyLikedPoemIds((prev) => new Set(prev).add(poemId));

    } catch (err) {
      console.error("Error sending like:", err);
    }
  };

  return (
    <Button
      variant="outline"
      className="px-6 shadow-sm bg-white"
      disabled={poemLoading || alreadyLiked}
      onClick={onClick}
    >
      <img
        src={(process.env.NEXT_PUBLIC_LINK_BASE || "/") + "svg/like.svg"}
        className="w-6 h-6 mr-2"
        alt="Like"
      />
      Líbí se mi
    </Button>
  );
}
