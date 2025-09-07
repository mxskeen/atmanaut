import Header from "@/components/header";
import "./globals.css";
import { Inter } from "next/font/google";
import { Toaster } from "sonner";
import "react-quill-new/dist/quill.snow.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "atmanaut",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
          <Header />
          <main>{children}</main>
          <Toaster position="bottom-center" />
        </div>
      </body>
    </html>
  );
}
