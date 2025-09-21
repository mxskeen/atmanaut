"use client";

import { useState, useEffect, useMemo } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { format, isSameDay } from "date-fns";
import { Calendar as CalendarIcon, Search } from "lucide-react";
import { cn } from "@/shared/utils";
import { MOODS } from "@/shared/moods";
import EntryCard from "@/components/entry-card";
import { useApiClient } from "@/lib/api-client";

export function JournalFilters({ entries }) {
  const apiClient = useApiClient();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedMood, setSelectedMood] = useState("");
  const [date, setDate] = useState(null);
  const [filteredEntries, setFilteredEntries] = useState(entries);
  const [semanticResults, setSemanticResults] = useState(null);
  const [semanticLoading, setSemanticLoading] = useState(false);

  // Debounced semantic search
  useEffect(() => {
    const doSearch = async () => {
      if (!searchQuery || searchQuery.trim().length < 2) {
        setSemanticResults(null);
        return;
      }
      try {
        setSemanticLoading(true);
        const res = await apiClient.semanticSearch({
          query: searchQuery,
          limit: 50,
          similarity_threshold: 0.2,
        });
        const results = res.results || res.data?.results || [];
        setSemanticResults(results);
      } catch (e) {
        console.error("Semantic search failed", e);
        setSemanticResults(null);
      } finally {
        setSemanticLoading(false);
      }
    };
    const t = setTimeout(doSearch, 300);
    return () => clearTimeout(t);
  }, [searchQuery]);

  // Apply filters and merge semantic results
  useEffect(() => {
    let base = entries;
    // If semantic results exist, prefer them (already filtered by similarity)
    if (semanticResults && semanticResults.length > 0) {
      const ids = new Set(semanticResults.map((r) => r.id));
      base = entries.filter((e) => ids.has(e.id));
      // Sort by semantic similarity if provided
      const scoreOf = (id) => {
        const r = semanticResults.find((x) => x.id === id);
        return r?.similarity_score ?? r?.combined_score ?? 0;
      };
      base.sort((a, b) => scoreOf(b.id) - scoreOf(a.id));
    } else if (searchQuery) {
      const q = searchQuery.toLowerCase();
      base = base.filter(
        (entry) =>
          entry.title.toLowerCase().includes(q) ||
          entry.content.toLowerCase().includes(q)
      );
    }

    // Apply mood filter
    if (selectedMood) {
      base = base.filter((entry) => entry.mood === selectedMood);
    }

    // Apply date filter
    if (date) {
      base = base.filter((entry) =>
        isSameDay(new Date(entry.createdAt), date)
      );
    }

    setFilteredEntries(base);
  }, [entries, searchQuery, selectedMood, date, semanticResults]);

  const clearFilters = () => {
    setSearchQuery("");
    setSelectedMood("");
    setDate(null);
  };

  return (
    <>
      {/* Filters */}
      <div className="flex flex-wrap gap-4">
        <div className="flex-1 min-w-[200px]">
          <Input
            placeholder="Search entries..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full"
            prefix={<Search className="h-4 w-4 text-gray-400" />}
          />
        </div>

        <Select value={selectedMood} onValueChange={setSelectedMood}>
          <SelectTrigger className="w-[150px]">
            <SelectValue placeholder="Filter by mood" />
          </SelectTrigger>
          <SelectContent>
            {Object.values(MOODS).map((mood) => (
              <SelectItem key={mood.id} value={mood.id}>
                <span className="flex items-center gap-2">
                  {mood.emoji} {mood.label}
                </span>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Popover>
          <PopoverTrigger asChild>
            <Button
              variant={"outline"}
              className={cn(
                "justify-start text-left font-normal",
                !date && "text-muted-foreground"
              )}
            >
              <CalendarIcon className="h-4 w-4" />
              {date ? format(date, "PPP") : <span>Pick a date</span>}
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-auto p-0">
            <Calendar
              mode="single"
              selected={date}
              onSelect={setDate}
              initialFocus
            />
          </PopoverContent>
        </Popover>

        {(searchQuery || selectedMood || date) && (
          <Button
            variant="ghost"
            onClick={clearFilters}
            className="text-orange-600"
          >
            Clear Filters
          </Button>
        )}
      </div>

      {/* Results Summary */}
      <div className="text-sm text-gray-500">
        {semanticLoading ? "Searching..." : `Showing ${filteredEntries.length} of ${entries.length} entries`}
      </div>

      {/* Entries List */}
      {filteredEntries.length === 0 ? (
        <div className="text-center p-8">
          <p className="text-gray-500">No entries found</p>
        </div>
      ) : (
        <div className="flex flex-col gap-4">
          {filteredEntries.map((entry) => (
            <EntryCard key={entry.id} entry={entry} />
          ))}
        </div>
      )}
    </>
  );
}
