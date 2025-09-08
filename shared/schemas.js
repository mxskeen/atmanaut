import { z } from "zod";

const today = new Date();
const oneYearFromNow = new Date();
oneYearFromNow.setFullYear(today.getFullYear() + 1);

export const journalSchema = z.object({
  title: z.string().min(1, "Title is required"),
  content: z.string().min(1, "Content is required"),
  mood: z.string().min(1, "Mood is required"),
  collectionId: z.string().optional(),
  sendToFutureDate: z
    .union([z.string(), z.date()])
    .optional()
    .refine(
      (dateVal) => {
        if (!dateVal || (typeof dateVal === "string" && dateVal.trim() === ""))
          return true;
        let date;
        if (dateVal instanceof Date) {
          date = dateVal;
        } else {
          date = new Date(dateVal);
        }
        return !isNaN(date) && date > today && date <= oneYearFromNow;
      },
      {
        message: "Date must be within 1 year from today and not in the past",
      }
    ),
});

export const collectionSchema = z.object({
  name: z.string().min(1, "Name is required"),
  description: z.string().optional(),
});
