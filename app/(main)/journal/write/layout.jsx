"use client";

import Link from "next/link";
import { Suspense, useState } from "react";
import { BarLoader } from "react-spinners";
import FutureEntryModal from "@/components/future-entry-modal";
import { useFutureEntries } from "@/hooks/use-future-entries";
import { MOODS } from "@/shared/moods";

export default function WriteLayout({ children }) {
  const { futureEntry, loading, markDelivered } = useFutureEntries();
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedMood, setSelectedMood] = useState("");
  const handleMoodChange = (e) => {
    setSelectedMood(e.target.value);
  };

  // Open modal when futureEntry is loaded and available
  if (!loading && futureEntry && !modalOpen) {
    setModalOpen(true);
  }

  const handleClose = () => {
    setModalOpen(false);
    if (futureEntry) {
      markDelivered(futureEntry.id);
    }
  };

  return (
    <div className="px-4 py-8">
      <div>
        <Link
          href="/dashboard"
          className="text-sm font-bold text-atmanaut-yellow hover:text-yellow-300 cursor-pointer transition-colors duration-200"
        >
          ← Back to Dashboard
        </Link>
      </div>
      <Suspense
        fallback={
          <BarLoader
            color="#ffe066"
            width={"100%"}
            speedMultiplier={1.2}
            height={6}
            className="mb-4 shadow-glow"
            style={{
              borderRadius: 8,
              boxShadow: "0 0 16px #ffe06688",
              transition: "all 0.5s cubic-bezier(0.4,0,0.2,1)",
            }}
          />
        }
      >
        {children}
      </Suspense>
      <FutureEntryModal
        entry={futureEntry}
        open={modalOpen}
        onClose={handleClose}
      />
    </div>
  );
}
