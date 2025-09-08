import { useEffect, useState } from "react";
import { useApiClient } from "@/lib/api-client";

export function useFutureEntries() {
  const apiClient = useApiClient();
  const [futureEntry, setFutureEntry] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchFutureEntry() {
      try {
        const res = await apiClient.get("/journal/future-entries/today");
        const entries = res?.data?.entries || [];
        if (entries.length > 0) {
          setFutureEntry(entries[0]);
        }
      } catch (e) {
        // fail silently
      } finally {
        setLoading(false);
      }
    }
    fetchFutureEntry();
  }, [apiClient]);

  const markDelivered = async (entryId) => {
    try {
      await apiClient.post(`/journal/future-entries/${entryId}/delivered`);
    } catch (e) {}
  };

  return { futureEntry, loading, markDelivered };
}
