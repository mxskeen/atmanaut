import Header from "@/components/header";
import FloatingParticles from "@/components/floating-particles";
import "./globals.css";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import { Toaster } from "sonner";
import "react-quill-new/dist/quill.snow.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "atmanaut",
  description: "",
};

export default function RootLayout({ children }) {
  return (
    <ClerkProvider
      dynamic
      // appearance={{
      //   baseTheme: shadesOfPurple,
      //   variables: {
      //     colorPrimary: "#3b82f6",
      //     colorBackground: "#1a202c",
      //     colorInputBackground: "#2D3748",
      //     colorInputText: "#F3F4F6",
      //   },
      //   elements: {
      //     formButtonPrimary: "bg-purple-600 hover:bg-purple-700 text-white",
      //     card: "bg-gray-800",
      //     headerTitle: "text-blue-400",
      //     headerSubtitle: "text-gray-400",
      //   },
      // }}
    >
      <html lang="en">
        <body
          suppressHydrationWarning={true}
          className={`${inter.className} zen-gradient text-atmanaut-cream`}
        >
          <FloatingParticles />
          <Header />
          <main
            suppressHydrationWarning={true}
            className="min-h-screen pt-20 md:pt-24 relative z-10"
          >
            {children}
          </main>
          <Toaster richColors />

          <footer className="bg-atmanaut-olive/20 py-12 backdrop-blur-sm">
            <div className="container mx-auto px-4 text-center text-atmanaut-cream">
              <p className="text-sm opacity-70">
                © 2025 Project Atmanaut - a voyager of the soul
              </p>
            </div>
          </footer>
        </body>
      </html>
    </ClerkProvider>
  );
}
