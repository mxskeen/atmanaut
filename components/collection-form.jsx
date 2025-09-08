"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { collectionSchema } from "@/shared/schemas";
import { BarLoader } from "react-spinners";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";

const CollectionForm = ({ onSuccess, loading, open, setOpen }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(collectionSchema),
    defaultValues: {
      name: "",
      description: "",
    },
  });

  const onSubmit = handleSubmit(async (data) => {
    onSuccess(data);
  });

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="bg-atmanaut-dark/95 border border-atmanaut-yellow/40 shadow-glow rounded-3xl max-w-lg mx-auto p-10 relative animate-zen-fade-in">
        <div
          className="absolute inset-0 pointer-events-none rounded-3xl z-0"
          style={{ boxShadow: "0 0 80px 0 #ffe06633" }}
        />
        <DialogHeader>
          <DialogTitle className="text-4xl font-extrabold text-atmanaut-yellow mb-6 text-center drop-shadow-xl tracking-tight">
            Create New Collection
          </DialogTitle>
        </DialogHeader>
        {loading && (
          <div className="mb-6">
            <BarLoader
              width={"100%"}
              color="#ffe066"
              speedMultiplier={1.2}
              height={5}
              style={{
                borderRadius: 8,
                boxShadow: "0 0 16px #ffe06688",
                transition: "all 0.5s cubic-bezier(0.4,0,0.2,1)",
              }}
            />
          </div>
        )}
        <form onSubmit={onSubmit} className="space-y-8 z-10 relative">
          <div className="space-y-2">
            <label className="text-lg font-bold text-atmanaut-yellow tracking-tight">
              Collection Name
            </label>
            <Input
              {...register("name")}
              placeholder="Enter collection name..."
              className={`bg-atmanaut-dark/80 border border-atmanaut-yellow/40 text-atmanaut-cream placeholder:text-atmanaut-cream/60 focus:border-atmanaut-yellow focus:ring-2 focus:ring-atmanaut-yellow/40 rounded-xl px-5 py-4 text-lg ${
                errors.name ? "border-red-500" : ""
              }`}
            />
            {errors.name && (
              <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
            )}
          </div>
          <div className="space-y-2">
            <label className="text-lg font-bold text-atmanaut-yellow tracking-tight">
              Description{" "}
              <span className="font-normal text-atmanaut-yellow/70">
                (Optional)
              </span>
            </label>
            <Textarea
              {...register("description")}
              placeholder="Describe your collection..."
              className={`bg-atmanaut-dark/80 border border-atmanaut-yellow/40 text-atmanaut-cream placeholder:text-atmanaut-cream/60 focus:border-atmanaut-yellow focus:ring-2 focus:ring-atmanaut-yellow/40 rounded-xl px-5 py-4 text-lg ${
                errors.description ? "border-red-500" : ""
              }`}
            />
            {errors.description && (
              <p className="text-red-500 text-sm mt-1">
                {errors.description.message}
              </p>
            )}
          </div>
          <div className="flex justify-center gap-8 pt-4">
            <Button
              type="button"
              className="bg-atmanaut-olive text-atmanaut-cream hover:bg-atmanaut-yellow hover:text-atmanaut-dark border border-atmanaut-yellow/40 shadow transition-all duration-300 px-8 py-3 rounded-xl font-semibold text-lg"
              onClick={() => setOpen(false)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="gradient-button text-atmanaut-dark font-bold shadow-glow border border-atmanaut-yellow/60 hover:bg-atmanaut-yellow/80 hover:text-atmanaut-dark transition-all duration-300 px-8 py-3 rounded-xl text-lg"
            >
              Create Collection
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default CollectionForm;
