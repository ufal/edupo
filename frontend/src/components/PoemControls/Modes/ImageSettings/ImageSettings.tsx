"use client";

import { usePoem } from "@/store/poemStore";
import { usePoemGenerator } from "@/hooks/usePoemGenerator";
import { useEffect, useState } from "react";

export default function ImageSettings() {
  const { currentValues } = usePoem();
  const { fetchImage } = usePoemGenerator();

  const [imagePath, setImagePath] = useState<string | null>(null);
  const [imageDesc, setImageDesc] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadImage = async () => {
      if (!currentValues.id) {
        setImagePath(null);
        setImageDesc(null);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const imgResp = await fetchImage(currentValues.id!);

        setImagePath(imgResp.url || null);
        setImageDesc(imgResp.description || null);

      } catch (err: any) {
        setImagePath(null);
        setImageDesc(null);
        setError(err.message || "Unknown error");

      } finally {
        setLoading(false);
      }
    };

    loadImage();
  }, [currentValues.id, fetchImage]);

  return (
    <div className="w-full px-docOffsetXSmall tablet:px-docOffsetXBig flex flex-col items-center justify-center py-4">
      {loading && <p className="text-gray-500 text-sm">Načítám obrázek…</p>}

      {error && (
        <p className="text-crimsonRed text-sm">Chyba při načítání obrázku: {error}</p>
      )}

      {!loading && !error && imagePath && (
        <img
          src={imagePath}
          alt={imageDesc ?? "Obrázek k básni"}
          title={imageDesc ?? "Obrázek k básni"}
          className="max-w-full h-auto rounded shadow"
        />
      )}

      {!loading && !error && !imagePath && (
        <p className="text-gray-500 text-sm">Žádný obrázek není k dispozici.</p>
      )}
    </div>
  );
}
