"use client";

import React, { useState, useEffect } from "react";
import {
  Calendar,
  ChevronRight,
  BarChart2,
  FileText,
  Heart,
  Brain,
  Leaf,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import TestimonialCarousel from "@/components/testimonial-carousel";
import ZenBreathingGuide from "@/components/zen-breathing-guide";
import { Skeleton } from "@/components/ui/skeleton";
import Link from "next/link";
import { apiClient } from "@/lib/api-client";
import faqs from "@/data/faqs";

const features = [
  {
    icon: Heart,
    title: "Mindful Journaling",
    description:
      "Express your thoughts with a zen-inspired editor designed for mindful reflection and inner peace.",
  },
  {
    icon: Brain,
    title: "Emotional Intelligence",
    description:
      "Track your emotional patterns with gentle analytics that help you understand your inner journey.",
  },
  {
    icon: Leaf,
    title: "Sacred Privacy",
    description:
      "Your thoughts are held in sacred trust with enterprise-grade security and complete privacy.",
  },
];

export default function LandingPage() {
  const [advice, setAdvice] = useState(null);

  useEffect(() => {
    const fetchAdvice = async () => {
      try {
        const dailyPrompt = await apiClient.getDailyPrompt();
        setAdvice(dailyPrompt.data || dailyPrompt); // Extract data field or use the response directly
      } catch (error) {
        console.error("Error fetching daily prompt:", error);
      } finally {
        setLoadingAdvice(false);
      }
    };

    fetchAdvice();
  }, []);

  return (
    <div
      suppressHydrationWarning
      className="relative container mx-auto px-4 pt-16 pb-16"
    >
      {/* Hero Section */}
      <div className="max-w-5xl mx-auto text-center space-y-8">
        <h1 className="text-5xl md:text-7xl lg:text-8xl gradient-title mb-6 animate-zen-fade-in">
          Your Sacred Space to Reflect. <br /> Your Soul&apos;s Story to Tell.
        </h1>
        <p className="text-lg md:text-xl text-atmanaut-cream/90 mb-8">
          Capture your thoughts, track your moods, and reflect on your journey
          in a beautiful, secure space.
        </p>
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-t from-atmanaut-cream/50 via-transparent to-transparent pointer-events-none z-10" />
          <div className="bg-atmanaut-dark/80 backdrop-blur-sm rounded-2xl p-4 max-full mx-auto shadow-glow border border-atmanaut-olive/30">
            <div className="border-b border-atmanaut-olive/50 pb-4 mb-4 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-atmanaut-cream" />
                <span className="text-atmanaut-cream font-medium">
                  Today&rsquo;s Entry
                </span>
              </div>
              <div className="flex gap-2">
                <div className="h-3 w-3 rounded-full bg-atmanaut-yellow" />
                <div className="h-3 w-3 rounded-full bg-atmanaut-olive" />
                <div className="h-3 w-3 rounded-full bg-atmanaut-dark-olive" />
              </div>
            </div>
            <div className="space-y-4 p-4">
              <h3 className="text-xl font-semibold text-atmanaut-cream">
                {advice ? advice : "My Thoughts Today"}
              </h3>
              <Skeleton className="h-4 bg-atmanaut-olive/30 rounded w-3/4" />
              <Skeleton className="h-4 bg-atmanaut-olive/30 rounded w-full" />
              <Skeleton className="h-4 bg-atmanaut-olive/30 rounded w-2/3" />
            </div>
          </div>
        </div>
        <div className="flex justify-center gap-4">
          <Link href="/dashboard">
            <Button
              variant="journal"
              className="px-8 py-6 rounded-full flex items-center gap-2 apple-hover-button"
            >
              Start Writing <ChevronRight className="h-5 w-5" />
            </Button>
          </Link>
          <Link href="#features">
            <Button
              variant="outline"
              className="px-8 py-6 rounded-full border-atmanaut-cream/60 text-atmanaut-dark hover:bg-atmanaut-yellow/20 hover:text-atmanaut-dark hover:border-atmanaut-yellow/60 apple-hover-button transition-all duration-300"
            >
              Learn More
            </Button>
          </Link>
        </div>
      </div>

      {/* Feature Cards */}
      <section
        id="features"
        className="mt-24 grid md:grid-cols-2 lg:grid-cols-3 gap-8"
      >
        {features.map((feature, index) => (
          <Card
            key={index}
            className="zen-card apple-hover animate-zen-fade-in"
            style={{ animationDelay: `${index * 0.2}s` }}
          >
            <CardContent className="p-6">
              <div className="h-12 w-12 bg-atmanaut-yellow/80 rounded-full flex items-center justify-center mb-4 shadow-glow animate-zen-pulse">
                <feature.icon className="h-6 w-6 text-atmanaut-dark" />
              </div>
              <h3 className="font-semibold text-xl text-atmanaut-cream mb-2 zen-text-glow">
                {feature.title}
              </h3>
              <p className="text-atmanaut-cream/70">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      <div className="space-y-24 mt-24">
        {/* Feature 1 */}
        <div className="grid md:grid-cols-2 gap-12 ">
          <div className="space-y-6">
            <div className="h-12 w-12 bg-atmanaut-yellow/80 rounded-full flex items-center justify-center shadow-glow apple-hover-subtle">
              <FileText className="h-6 w-6 text-atmanaut-dark" />
            </div>
            <h3 className="text-2xl font-bold text-atmanaut-cream">
              Rich Text Editor
            </h3>
            <p className="text-lg text-atmanaut-cream/70">
              Express yourself fully with our powerful editor featuring:
            </p>
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-atmanaut-yellow" />
                <span className="text-atmanaut-cream/80">
                  Format text with ease
                </span>
              </li>
              <li className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-atmanaut-yellow" />
                <span className="text-atmanaut-cream/80">Embed links</span>
              </li>
            </ul>
          </div>
          <div className="space-y-4 bg-atmanaut-dark/80 backdrop-blur-sm rounded-2xl shadow-glow p-6 border border-atmanaut-olive/30">
            {/* Editor Preview */}
            <div className="flex gap-2 mb-6">
              <div className="h-8 w-8 rounded bg-atmanaut-yellow/60"></div>
              <div className="h-8 w-8 rounded bg-atmanaut-olive/60"></div>
              <div className="h-8 w-8 rounded bg-atmanaut-dark-olive/60"></div>
            </div>
            <div className="h-4 bg-atmanaut-olive/30 rounded w-3/4"></div>
            <div className="h-4 bg-atmanaut-olive/30 rounded w-full"></div>
            <div className="h-4 bg-atmanaut-olive/30 rounded w-2/3"></div>
            <div className="h-4 bg-atmanaut-olive/30 rounded w-1/3"></div>
          </div>
        </div>

        {/* Feature 2 */}
        <div className="grid md:grid-cols-2 gap-12 md:flex-row-reverse">
          <div className="space-y-6 md:order-2">
            <div className="h-12 w-12 bg-atmanaut-yellow/80 rounded-full flex items-center justify-center shadow-glow apple-hover-subtle">
              <BarChart2 className="h-6 w-6 text-atmanaut-dark" />
            </div>
            <h3 className="text-2xl font-bold text-atmanaut-cream">
              Mood Analytics
            </h3>
            <p className="text-lg text-atmanaut-cream/70">
              Track your emotional journey with powerful analytics:
            </p>
            <ul className="space-y-3">
              <li className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-atmanaut-yellow" />
                <span className="text-atmanaut-cream/80">
                  Visual mood trends
                </span>
              </li>
              <li className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-atmanaut-yellow" />
                <span className="text-atmanaut-cream/80">
                  Pattern recognition
                </span>
              </li>
            </ul>
          </div>
          <div className="space-y-4 bg-atmanaut-dark/80 backdrop-blur-sm rounded-2xl shadow-glow p-6 border border-atmanaut-olive/30 md:order-1">
            {/* Analytics Preview */}
            <div className="h-40 bg-gradient-to-t from-atmanaut-olive/30 to-atmanaut-yellow/20 rounded-lg"></div>
            <div className="flex justify-between">
              <div className="h-4 w-16 bg-atmanaut-yellow/60 rounded"></div>
              <div className="h-4 w-16 bg-atmanaut-olive/60 rounded"></div>
              <div className="h-4 w-16 bg-atmanaut-dark-olive/60 rounded"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Play to Calm Your Nervous System */}
      <div className="mt-24 flex justify-center">
        <ZenBreathingGuide />
      </div>

      {/* Testimonials Carousel */}
      <TestimonialCarousel />

      {/* FAQ Section */}
      <div className="mt-24">
        <h2 className="text-3xl font-bold text-center text-atmanaut-cream mb-12">
          Frequently Asked Questions
        </h2>
        <Accordion type="single" collapsible className="w-full mx-auto">
          {faqs.map((faq, index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger className="text-atmanaut-cream text-lg">
                {faq.q}
              </AccordionTrigger>
              <AccordionContent className="text-atmanaut-cream/70">
                {faq.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>

      {/* CTA Section */}
      <div className="mt-24">
        <Card className="bg-atmanaut-dark/80 backdrop-blur-sm border border-atmanaut-olive/30 shadow-glow">
          <CardContent className="p-12 text-center">
            <h2 className="text-3xl font-bold text-atmanaut-cream mb-6">
              Start atmanaut-ing on Your Journey Today
            </h2>
            <p className="text-lg text-atmanaut-cream/70 mb-8 max-w-2xl mx-auto">
              Join thousands of writers who have already discovered the power of
              digital journaling.
            </p>
            <Button
              size="lg"
              variant="journal"
              className="animate-bounce-slow apple-hover-button"
            >
              Get Started for Free <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
