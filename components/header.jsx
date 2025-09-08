"use client";

import React from "react";
import { Button } from "./ui/button";
import Link from "next/link";
import { PenBox, FolderOpen } from "lucide-react";
import Image from "next/image";
import { SignedIn, SignedOut, SignInButton } from "@clerk/nextjs";
import UserMenu from "./user-menu";

function Header() {
  return (
    <header
      suppressHydrationWarning={true}
      className="fixed top-0 left-0 right-0 z-50 w-full"
      style={{
        boxShadow: "0 4px 24px 0 rgba(247,237,59,0.10), 0 1.5px 0 0 #ffe066",
      }}
    >
      <nav
        suppressHydrationWarning={true}
        className="py-4 md:py-6 px-4 flex justify-between items-center backdrop-blur-sm bg-atmanaut-dark/95 border-b border-atmanaut-olive/20 container mx-auto"
      >
        <Link href="/" className="flex items-center">
          <Image
            src={"/logo.png"}
            alt="atmanaut Logo"
            width={280}
            height={90}
            className="h-10 w-auto object-contain"
          />
        </Link>
        <div
          suppressHydrationWarning={true}
          className="flex items-center gap-4"
        >
          <SignedIn>
            <Link href="/dashboard#collections">
              <Button
                variant="outline"
                size="sm"
                className="flex items-center gap-2 apple-hover-button border-atmanaut-yellow/70 text-atmanaut-yellow bg-atmanaut-dark/90 hover:bg-atmanaut-yellow/20 hover:text-atmanaut-dark hover:border-atmanaut-yellow/90 transition-all duration-300 shadow-glow"
                style={{ fontWeight: 600, boxShadow: "0 0 8px #ffe06688" }}
              >
                <FolderOpen size={16} />
                <span className="hidden md:inline">Collections</span>
              </Button>
            </Link>
          </SignedIn>
          <Link href="/journal/write">
            <Button
              variant="journal"
              size="sm"
              className="flex items-center gap-2 apple-hover-button hover:shadow-atmanaut-yellow/40 transition-all duration-300"
            >
              <PenBox size={16} />
              <span className="hidden md:inline">Write New</span>
            </Button>
          </Link>
          <SignedOut>
            <SignInButton forceRedirectUrl="/dashboard">
              <Button
                variant="outline"
                size="sm"
                className="apple-hover-button border-atmanaut-olive/40 text-atmanaut-dark hover:bg-atmanaut-yellow/20 hover:text-atmanaut-dark hover:border-atmanaut-yellow/60 transition-all duration-300"
              >
                Login
              </Button>
            </SignInButton>
          </SignedOut>
          <SignedIn>
            <UserMenu />
          </SignedIn>
        </div>
      </nav>
    </header>
  );
}

export default Header;
