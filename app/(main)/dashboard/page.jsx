"use client";

import { useState, useEffect } from "react";
import { useApiClient } from "@/lib/api-client";
import MoodAnalytics from "./_components/mood-analytics";
import Collections from "./_components/collections";
import { useFutureEntries } from "@/hooks/use-future-entries";
import FutureEntryModal from "@/components/future-entry-modal";

const Dashboard = () => {
  const apiClient = useApiClient();
  const [collections, setCollections] = useState([]);
  const [entriesByCollection, setEntriesByCollection] = useState({});
  const [loading, setLoading] = useState(true);

  // Future entry modal logic
  const {
    futureEntry,
    loading: futureLoading,
    markDelivered,
  } = useFutureEntries();
  const [showFutureModal, setShowFutureModal] = useState(false);

  useEffect(() => {
    if (futureEntry) {
      setShowFutureModal(true);
      markDelivered(futureEntry.id);
    }
  }, [futureEntry]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [collectionsData, entriesData] = await Promise.all([
          apiClient.getCollections(),
          apiClient.getCollectionEntries("all"), // Get all entries
        ]);

        setCollections(collectionsData.data || []);

        // Group entries by collection
        const entriesByCollection =
          entriesData?.data?.entries?.reduce((acc, entry) => {
            const collectionId = entry.collectionId || "unorganized";
            if (!acc[collectionId]) {
              acc[collectionId] = [];
            }
            acc[collectionId].push(entry);
            return acc;
          }, {}) || {};

        setEntriesByCollection(entriesByCollection);
      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [apiClient]);

  if (loading || futureLoading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <FutureEntryModal
        entry={futureEntry}
        open={showFutureModal}
        onClose={() => setShowFutureModal(false)}
      />
      <div className="px-4 py-8 space-y-8">
        {/* Analytics Section */}
        <section className="space-y-4">
          <MoodAnalytics />
        </section>

        <Collections
          collections={collections}
          entriesByCollection={entriesByCollection}
        />
      </div>
    </>
  );
};

export default Dashboard;
