"use client";

import React, { useState, useEffect } from "react";
import { useApiClient } from "@/lib/api-client";
import { toast } from "sonner";
import CollectionPreview from "./collection-preview";
import CollectionForm from "@/components/collection-form";
import useFetch from "@/hooks/use-fetch";

const Collections = ({ collections = [], entriesByCollection }) => {
  const apiClient = useApiClient();
  const [isCollectionDialogOpen, setIsCollectionDialogOpen] = useState(false);

  const {
    loading: createCollectionLoading,
    fn: createCollectionFn,
    data: createdCollection,
  } = useFetch((data) => apiClient.createCollection(data));

  useEffect(() => {
    if (createdCollection) {
      setIsCollectionDialogOpen(false);
      fetchCollections(); // Refresh collections list
      toast.success(`Collection ${createdCollection.name} created!`);
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [createdCollection, createCollectionLoading]);

  const handleCreateCollection = async (data) => {
    createCollectionFn(data);
  };

  // Always show the two folders (Organized / Unorganized)

  return (
    <section id="collections" className="space-y-6">
      <h2 className="text-3xl font-bold gradient-title">Collections</h2>
      <div className="grid gap-6 md:grid-cols-2">
        {/* Organized folder aggregates all collections */}
        <CollectionPreview
          id="organized"
          name="Organized"
          entries={collections.flatMap((c) => entriesByCollection[c.id] || [])}
        />

        {/* Unorganized folder always visible */}
        <CollectionPreview
          name="Unorganized"
          entries={entriesByCollection?.unorganized || []}
          isUnorganized={true}
        />
      </div>
    </section>
  );
};

export default Collections;
