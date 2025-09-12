"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { QrCode } from "lucide-react"
import { QRCodeSVG } from "qrcode.react"

export default function QrCodeButton() {
  const [open, setOpen] = useState(false)
  const currentUrl = typeof window !== "undefined" ? window.location.href : ""

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          className="text-slate-800"
          onClick={() => setOpen(true)}
        >
          <QrCode />
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>QR kód pro tuto báseň</DialogTitle>
        </DialogHeader>
        <div className="flex justify-center items-center py-4">
          <QRCodeSVG value={currentUrl} size={200} />
        </div>
      </DialogContent>
    </Dialog>
  )
}
