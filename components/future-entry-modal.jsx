import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ConfettiAnimation } from "./confetti-animation"; // You can implement this or use a package

export default function FutureEntryModal({ entry, open, onClose }) {
  if (!entry) return null;
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="glass-effect max-w-lg mx-auto p-8 rounded-2xl shadow-glow text-center animate-zen-fade-in">
        <ConfettiAnimation />
        <DialogHeader>
          <DialogTitle className="gradient-title text-3xl mb-2">
            A message from your past self!
          </DialogTitle>
        </DialogHeader>
        <div className="text-lg text-atmanaut-cream/90 mb-4">
          <span className="font-semibold">{entry.title}</span>
        </div>
        <div
          className="bg-atmanaut-dark/70 rounded-lg p-4 mb-6 text-atmanaut-cream/80 prose prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: entry.content }}
        />
        <Button onClick={onClose} className="gradient-button mt-2">
          Close
        </Button>
      </DialogContent>
    </Dialog>
  );
}
