import React from "react";
import { Card, CardContent } from "./ui/card";
import Link from "next/link";
import { format } from "date-fns";

const EntryCard = ({ entry }) => {
  return (
    <Link href={`/journal/${entry.id}`}>
      <Card className="gradient-card hover:shadow-glow transition-all duration-300 border border-atmanaut-cream/30 hover-lift">
        <CardContent className="p-6">
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <span className="text-2xl">{entry.moodData.emoji}</span>
                <h3 className="font-semibold text-lg text-atmanaut-dark">
                  {entry.title}
                </h3>
              </div>
              <div
                className="text-atmanaut-dark/70 line-clamp-2"
                dangerouslySetInnerHTML={{ __html: entry.content }}
              />
            </div>
            <time className="text-sm text-atmanaut-dark/60">
              {format(new Date(entry.createdAt), "MMM d, yyyy")}
            </time>
          </div>
          {entry.collection && (
            <div className="mt-4 flex items-center gap-2">
              <span className="text-sm px-2 py-1 bg-atmanaut-yellow/80 text-atmanaut-dark rounded-lg font-medium">
                {entry.collection.name}
              </span>
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
};

export default EntryCard;
