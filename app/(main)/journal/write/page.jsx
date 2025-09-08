"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import dynamic from "next/dynamic";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import useFetch from "@/hooks/use-fetch";
import { Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useApiClient } from "@/lib/api-client";
import { getMoodById, MOODS } from "@/shared/moods";
import { BarLoader } from "react-spinners";
import { toast } from "sonner";
import { journalSchema } from "@/shared/schemas";
import "react-quill-new/dist/quill.snow.css";
import CollectionForm from "@/components/collection-form";

const ReactQuill = dynamic(() => import("react-quill-new"), { ssr: false });

export default function JournalEntryPage() {
  const apiClient = useApiClient();
  const router = useRouter();
  const searchParams = useSearchParams();
  const editId = searchParams.get("edit");
  const [isCollectionDialogOpen, setIsCollectionDialogOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  // For error display
  const [formError, setFormError] = useState("");

  // Fetch Hooks
  const {
    loading: collectionsLoading,
    data: collectionsResponse,
    fn: fetchCollections,
  } = useFetch(() => apiClient.getCollections());

  const collections = collectionsResponse?.data || collectionsResponse || [];

  const {
    loading: entryLoading,
    data: existingEntryResponse,
    fn: fetchEntry,
  } = useFetch((id) => apiClient.getEntry(id));

  const existingEntry = existingEntryResponse?.data || existingEntryResponse;

  const {
    loading: draftLoading,
    data: draftData,
    fn: fetchDraft,
  } = useFetch(() => apiClient.getDraft());

  const { loading: savingDraft, fn: saveDraftFn } = useFetch((data) =>
    apiClient.saveDraft(data)
  );

  const {
    loading: actionLoading,
    fn: actionFn,
    data: actionResult,
  } = useFetch(
    isEditMode
      ? (data) => apiClient.updateEntry(editId, data)
      : (data) => apiClient.createEntry(data)
  );

  const {
    loading: createCollectionLoading,
    fn: createCollectionFn,
    data: createdCollection,
  } = useFetch((data) => apiClient.createCollection(data));

  const {
    register,
    handleSubmit,
    control,
    setValue,
    getValues,
    watch,
    reset,
    formState: { errors, isDirty },
  } = useForm({
    resolver: zodResolver(journalSchema),
    defaultValues: {
      title: "",
      content: "",
      mood: "",
      collectionId: "",
      sendToFutureDate: undefined,
    },
  });

  // Handle draft or existing entry loading
  useEffect(() => {
    fetchCollections();
    if (editId) {
      setIsEditMode(true);
      fetchEntry(editId);
    } else {
      setIsEditMode(false);
      fetchDraft();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editId, fetchCollections, fetchDraft, fetchEntry]);

  // Handle setting form data from draft
  useEffect(() => {
    if (isEditMode && existingEntry) {
      reset({
        title: existingEntry.title || "",
        content: existingEntry.content || "",
        mood: existingEntry.mood || "",
        collectionId: existingEntry.collectionId || "",
        sendToFutureDate: existingEntry.sendToFutureDate
          ? typeof existingEntry.sendToFutureDate === "string"
            ? existingEntry.sendToFutureDate.split("T")[0]
            : undefined
          : undefined,
      });
    } else if (draftData?.success && draftData?.data) {
      reset({
        title: draftData.data.title || "",
        content: draftData.data.content || "",
        mood: draftData.data.mood || "",
        collectionId: "",
        sendToFutureDate: draftData.data.sendToFutureDate
          ? typeof draftData.data.sendToFutureDate === "string"
            ? draftData.data.sendToFutureDate.split("T")[0]
            : undefined
          : undefined,
      });
    } else {
      reset({
        title: "",
        content: "",
        mood: "",
        collectionId: "",
        sendToFutureDate: undefined,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [draftData, isEditMode, existingEntry, reset]);

  // Handle collection creation success
  useEffect(() => {
    if (createdCollection) {
      setIsCollectionDialogOpen(false);
      fetchCollections();
      setValue("collectionId", createdCollection.id);
      toast.success(`Collection ${createdCollection.name} created!`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [createdCollection, fetchCollections, setValue]);

  // Handle successful submission
  useEffect(() => {
    if (actionResult && !actionLoading) {
      // Clear draft after successful publish
      if (!isEditMode) {
        saveDraftFn({ title: "", content: "", mood: "" });
      }

      router.push(
        `/collection/${
          actionResult.collectionId ? actionResult.collectionId : "unorganized"
        }`
      );

      toast.success(
        `Entry ${isEditMode ? "updated" : "created"} successfully!`
      );
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actionResult, actionLoading, isEditMode, router, saveDraftFn]);

  const onSubmit = handleSubmit(async (data) => {
    setFormError("");
    try {
      const mood = getMoodById(data.mood);
      // Always send sendToFutureDate as ISO string if set
      let sendToFutureDate = data.sendToFutureDate;
      if (
        typeof sendToFutureDate === "string" &&
        sendToFutureDate.trim() !== ""
      ) {
        const date = new Date(sendToFutureDate);
        if (!isNaN(date)) {
          sendToFutureDate = date.toISOString();
        } else {
          sendToFutureDate = undefined;
        }
      } else {
        sendToFutureDate = undefined;
      }
      await actionFn({
        ...data,
        sendToFutureDate,
        moodScore: mood.score,

        ...(isEditMode && { id: editId }),
      });
    } catch (err) {
      setFormError(err?.message || "Failed to submit entry");
    }
  });

  const formData = watch();

  const handleSaveDraft = async () => {
    if (!isDirty) {
      toast.error("No changes to save");
      return;
    }
    const result = await saveDraftFn(formData);
    if (result?.success) {
      toast.success("Draft saved successfully");
    }
  };

  const handleCreateCollection = async (data) => {
    createCollectionFn(data);
  };

  const isLoading =
    collectionsLoading ||
    entryLoading ||
    draftLoading ||
    actionLoading ||
    savingDraft;

  return (
    <>
      {/* Loading Bar - fixed at the very top of the viewport */}
      {isLoading && (
        <div className="fixed top-0 left-0 w-full z-[100]">
          <BarLoader
            width={"100%"}
            color="#ffe066"
            speedMultiplier={1.2}
            height={5}
            style={{
              borderRadius: 0,
              boxShadow: "0 2px 12px #ffe06688",
              transition: "all 0.3s cubic-bezier(0.4,0,0.2,1)",
            }}
          />
        </div>
      )}
      <div className="container mx-auto px-4 py-12">
        {/* Removed Back to Dashboard button for cleaner UI */}
        {/* Removed yellow line above main content */}
        <form
          onSubmit={onSubmit}
          className="space-y-6 mx-auto max-w-2xl bg-atmanaut-dark/90 border border-atmanaut-yellow/30 shadow-glow rounded-2xl p-8"
          style={{ backdropFilter: "blur(6px)" }}
        >
          <h1 className="text-5xl md:text-6xl gradient-title mb-2">
            {isEditMode ? "Edit Entry" : "What's on your mind?"}
          </h1>
          <p className="text-lg text-atmanaut-cream/80 mb-8">
            Jot down your thoughts, feelings, and memories. Your space, your
            pace.
          </p>
          {formError && (
            <div className="mb-4 p-3 rounded-lg bg-red-900/80 text-red-200 border border-red-400 text-center">
              {formError}
            </div>
          )}

          <div className="space-y-2">
            <label className="text-sm font-medium">Title</label>
            <Input
              disabled={isLoading}
              {...register("title")}
              placeholder="Give your entry a title..."
              className={`py-5 md:text-md ${
                errors.title ? "border-red-500" : ""
              }`}
            />
            {errors.title && (
              <p className="text-red-500 text-sm">{errors.title.message}</p>
            )}
          </div>

          {/* Send to Future Me */}
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2">
              <span>Send to Future Me</span>
              <span className="text-xs text-atmanaut-yellow/80">
                (optional)
              </span>
            </label>
            <Controller
              name="sendToFutureDate"
              control={control}
              render={({ field }) => {
                // Always use yyyy-mm-dd for value, min, max
                const today = new Date();
                const min = today.toISOString().split("T")[0];
                const maxDate = new Date();
                maxDate.setFullYear(today.getFullYear() + 1);
                const max = maxDate.toISOString().split("T")[0];
                // Ensure value is yyyy-mm-dd or empty string
                let value = field.value;
                if (value instanceof Date) {
                  value = value.toISOString().split("T")[0];
                } else if (typeof value === "string" && value.includes("T")) {
                  value = value.split("T")[0];
                } else if (!value) {
                  value = "";
                }
                return (
                  <Input
                    {...field}
                    type="date"
                    min={min}
                    max={max}
                    value={value}
                    placeholder="yyyy-mm-dd"
                    disabled={isLoading}
                    className={`py-5 md:text-md ${
                      errors.sendToFutureDate ? "border-red-500" : ""
                    }`}
                  />
                );
              }}
            />
            {errors.sendToFutureDate && (
              <p className="text-red-500 text-sm mt-1">
                {errors.sendToFutureDate.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">How are you feeling?</label>
            <Controller
              name="mood"
              control={control}
              render={({ field }) => (
                <Select onValueChange={field.onChange} value={field.value}>
                  <SelectTrigger
                    className={
                      (errors.mood ? "border-red-500 " : "") +
                      "py-1 px-2 text-xs bg-atmanaut-dark/95 border border-atmanaut-yellow/60 rounded-lg shadow focus:outline-none focus:ring-2 focus:ring-atmanaut-yellow transition-all duration-150 hover:bg-atmanaut-yellow/10 flex items-center gap-1 overflow-hidden whitespace-nowrap h-8"
                    }
                    style={{
                      minWidth: 200,
                      fontWeight: 500,
                      lineHeight: "1rem",
                    }}
                  >
                    <SelectValue
                      placeholder="Select a mood..."
                      className="flex items-center gap-1 text-xs truncate max-w-[180px]"
                    />
                  </SelectTrigger>
                  <SelectContent
                    className="max-h-60 overflow-y-auto bg-atmanaut-dark border border-atmanaut-yellow/60 rounded-lg shadow-lg animate-fade-in z-50 scrollbar-thin scrollbar-thumb-atmanaut-yellow/30 scrollbar-track-transparent"
                    style={{
                      scrollBehavior: "smooth",
                      padding: "0.25rem 0",
                      scrollbarWidth: "thin",
                      scrollbarColor: "rgba(255, 224, 102, 0.3) transparent",
                    }}
                  >
                    {Object.values(MOODS).map((mood) => (
                      <SelectItem
                        key={mood.id}
                        value={mood.id}
                        className="py-2 px-3 hover:bg-atmanaut-yellow/20 cursor-pointer rounded flex items-center gap-2 text-sm transition-colors duration-100 font-semibold text-atmanaut-yellow"
                      >
                        <span
                          className="w-6 h-6 flex items-center justify-center rounded-full text-xl mr-2 border border-atmanaut-yellow/40"
                          style={{
                            background: `var(--mood-color-${mood.color}, #222)`,
                          }}
                        >
                          {mood.emoji}
                        </span>
                        <span className="tracking-wide">{mood.label}</span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.mood && (
              <p className="text-red-500 text-sm">{errors.mood.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              {getMoodById(getValues("mood"))?.prompt ??
                "Write your thoughts..."}
            </label>
            <Controller
              name="content"
              control={control}
              render={({ field }) => (
                <div className="rounded-lg border border-atmanaut-yellow/30 bg-atmanaut-dark/70 focus-within:border-atmanaut-yellow transition-all duration-200">
                  <ReactQuill
                    readOnly={isLoading}
                    theme="snow"
                    value={field.value}
                    onChange={field.onChange}
                    modules={{
                      toolbar: [
                        [{ header: [1, 2, 3, false] }],
                        ["bold", "italic", "underline", "strike"],
                        [{ list: "ordered" }, { list: "bullet" }],
                        ["blockquote", "code-block"],
                        ["link"],
                        ["clean"],
                      ],
                    }}
                    className="min-h-[120px] max-h-[320px] text-base"
                  />
                </div>
              )}
            />
            {errors.content && (
              <p className="text-red-500 text-sm">{errors.content.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">
              Add to Collection (Optional)
            </label>
            <Controller
              name="collectionId"
              control={control}
              render={({ field }) => (
                <Select
                  onValueChange={(value) => {
                    if (value === "new") {
                      setIsCollectionDialogOpen(true);
                    } else {
                      field.onChange(value);
                    }
                  }}
                  value={field.value}
                >
                  <SelectTrigger className="bg-atmanaut-dark/80 focus:ring-2 focus:ring-atmanaut-yellow border-none">
                    <SelectValue placeholder="Choose a collection..." />
                  </SelectTrigger>
                  <SelectContent>
                    {collections?.map((collection) => (
                      <SelectItem key={collection.id} value={collection.id}>
                        <span className="text-base">{collection.name}</span>
                      </SelectItem>
                    ))}
                    <SelectItem value="new">
                      <span className="text-atmanaut-yellow font-semibold">
                        + Create New Collection
                      </span>
                    </SelectItem>
                  </SelectContent>
                </Select>
              )}
            />
          </div>

          <div className="space-x-4 flex mt-4">
            {!isEditMode && (
              <Button
                type="button"
                className="bg-atmanaut-yellow text-atmanaut-dark hover:bg-atmanaut-olive hover:text-atmanaut-cream border border-atmanaut-olive/40 transition-all duration-300 px-6 py-2 rounded-lg shadow"
                onClick={handleSaveDraft}
                disabled={savingDraft || !isDirty}
              >
                {savingDraft && (
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                )}
                Save as Draft
              </Button>
            )}
            <Button
              type="submit"
              className="bg-atmanaut-yellow text-atmanaut-dark font-semibold shadow-glow border border-atmanaut-yellow/60 hover:bg-atmanaut-yellow/80 hover:text-atmanaut-dark transition-all duration-300 px-6 py-2 rounded-lg shadow"
              disabled={actionLoading || !isDirty}
            >
              {isEditMode ? "Update Entry" : "Publish"}
            </Button>
          </div>
        </form>
        <CollectionForm
          loading={createCollectionLoading}
          onSuccess={handleCreateCollection}
          open={isCollectionDialogOpen}
          setOpen={setIsCollectionDialogOpen}
        />
      </div>
    </>
  );
}
