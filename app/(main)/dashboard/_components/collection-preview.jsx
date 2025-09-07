"use client";

import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import { Plus } from "lucide-react";
import { getMoodById } from "@/shared/moods";

const colorSchemes = {
  unorganized: {
    bg: "gradient-card hover:bg-atmanaut-cream/50 shadow-glow",
    tab: "bg-atmanaut-olive group-hover:bg-atmanaut-dark-olive",
  },
  collection: {
    bg: "gradient-card hover:bg-atmanaut-cream/50 shadow-glow",
    tab: "bg-atmanaut-yellow group-hover:bg-atmanaut-cream",
  },
  createCollection: {
    bg: "bg-atmanaut-olive/20 hover:bg-atmanaut-olive/30 shadow-glow",
    tab: "bg-atmanaut-olive/40 hover:bg-atmanaut-olive/60",
  },
};

const FolderTab = ({ colorClass }) => (
  <div
    className={`absolute inset-x-4 -top-2 h-2 rounded-t-md transform -skew-x-6 transition-colors ${colorClass}`}
  />
);

const EntryPreview = ({ entry }) => (
  <div className="bg-white/70 backdrop-blur-sm p-2 rounded-lg text-sm truncate text-atmanaut-dark border border-atmanaut-cream/30">
    <span className="mr-2">{getMoodById(entry.mood)?.emoji}</span>
    {entry.title}
  </div>
);

const CollectionPreview = ({
  id,
  name,
  entries = [],
  isUnorganized = false,
  isCreateNew = false,
  onCreateNew,
}) => {
  if (isCreateNew) {
    return (
      <button
        onClick={onCreateNew}
        className="group relative h-[200px] cursor-pointer"
      >
        <FolderTab colorClass={colorSchemes["createCollection"].bg} />
        <div
          className={`relative h-full rounded-lg p-6 shadow-md hover:shadow-lg transition-all apple-hover animate-zen-fade-in flex flex-col items-center justify-center gap-4 ${colorSchemes["createCollection"].tab}`}
        >
          <div className="h-12 w-12 rounded-full bg-atmanaut-yellow/80 group-hover:bg-atmanaut-yellow flex items-center justify-center shadow-glow animate-float">
            <Plus className="h-6 w-6 text-atmanaut-dark" />
          </div>
          <p className="text-atmanaut-dark font-medium">
            Create New Collection
          </p>
        </div>
      </button>
    );
  }

  return (
    <Link
      href={`/collection/${isUnorganized ? "unorganized" : id}`}
      className="group relative"
    >
      <FolderTab
        colorClass={
          colorSchemes[isUnorganized ? "unorganized" : "collection"].tab
        }
      />
      <div
        className={`relative rounded-lg p-6 shadow-md hover:shadow-lg transition-all apple-hover animate-zen-fade-in ${
          colorSchemes[isUnorganized ? "unorganized" : "collection"].bg
        }`}
      >
        <div className="flex items-center gap-3 mb-4">
          <span className="text-2xl">{isUnorganized ? "📂" : "📁"}</span>
          <h3 className="text-lg font-semibold truncate text-atmanaut-dark">
            {name}
          </h3>
        </div>
        <div className="space-y-2">
          <div className="flex justify-between text-sm text-atmanaut-dark/70">
            <span>{entries.length} entries</span>
            {entries.length > 0 && (
              <span>
                {formatDistanceToNow(new Date(entries[0].createdAt), {
                  addSuffix: true,
                })}
              </span>
            )}
          </div>
          <div className="space-y-2 mt-4">
            {entries.length > 0 ? (
              entries
                .slice(0, 2)
                .map((entry) => <EntryPreview key={entry.id} entry={entry} />)
            ) : (
              <p className="text-sm text-atmanaut-dark/50 italic">
                No entries yet
              </p>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default CollectionPreview;
