"use client";

import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import { useApiClient } from "@/lib/api-client";
import { JournalFilters } from "./_components/journal-filters";
import DeleteCollectionDialog from "./_components/delete-collection";

export default function CollectionPage() {
  const apiClient = useApiClient();
  const { collectionId } = useParams();
  const [entries, setEntries] = useState(null);
  const [collections, setCollections] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const entriesData = await apiClient.getCollectionEntries(collectionId);
        setEntries(entriesData.data || entriesData);
        
        if (collectionId !== "unorganized") {
          const collectionsData = await apiClient.getCollections();
          setCollections(collectionsData.data || collectionsData);
        }
      } catch (error) {
        console.error("Error fetching collection data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [collectionId]);

  if (loading) {
    return <div>Loading...</div>;
  }

  // Handle case where data might be undefined or have different structure
  const entriesArray = entries?.data?.entries || entries?.entries || entries || [];
  const collection = collections?.find((c) => c.id === collectionId);

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between">
        <div className="flex justify-between">
          <h1 className="text-4xl font-bold gradient-title">
            {collectionId === "unorganized"
              ? "Unorganized Entries"
              : collection?.name || "Collection"}
          </h1>
          {collection && (
            <DeleteCollectionDialog
              collection={collection}
              entriesCount={entriesArray.length}
            />
          )}
        </div>
        {collection?.description && (
          <h2 className="font-extralight pl-1">{collection?.description}</h2>
        )}
      </div>

      {/* Client-side Filters Component */}
      <JournalFilters entries={entriesArray} />
    </div>
  );
}
