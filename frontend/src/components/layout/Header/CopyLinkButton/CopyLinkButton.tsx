"use client"

import { Button } from "@/components/ui/button";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { LinkIcon } from "lucide-react";
import { useState } from "react";

export default function CopyLinkButton() {
  const [copied, setCopied] = useState(false);

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error("Failed to copy link", err);
    }
  }

  return (
    <TooltipProvider>
      <Tooltip open={copied} delayDuration={0}>
        <TooltipTrigger asChild>
          <Button
            variant="outline"
            size="icon"
            className="text-slate-800"
            onClick={handleCopyLink}>
            <LinkIcon />
          </Button>
        </TooltipTrigger>
        <TooltipContent>
          {copied ? "Zkopírováno do schránky!" : "Zkopírovat odkaz"}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
