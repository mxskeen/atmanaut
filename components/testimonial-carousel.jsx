"use client";

import React from "react";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "./ui/carousel";
import Autoplay from "embla-carousel-autoplay";
import { Card, CardContent } from "./ui/card";
import testimonials from "@/data/testimonials";

const TestimonialCarousel = () => {
  return (
    <div suppressHydrationWarning={true} className="mt-24">
      <h2 className="text-3xl font-bold text-center text-atmanaut-cream mb-12">
        What Our Writers Say
      </h2>
      <Carousel
        plugins={[
          Autoplay({
            delay: 2000,
          }),
        ]}
        className="w-full mx-auto"
      >
        <CarouselContent>
          {testimonials.map((testimonial, index) => (
            <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3">
              <Card className="bg-atmanaut-dark/80 backdrop-blur-sm border border-atmanaut-olive/30 shadow-glow hover-lift">
                <CardContent className="p-6">
                  <blockquote className="space-y-4">
                    <p className="text-atmanaut-cream/90 italic">
                      {`"${testimonial.text}"`}
                    </p>
                    <footer>
                      <div className="font-semibold text-atmanaut-yellow">
                        {testimonial.author}
                      </div>
                      <div className="text-sm text-atmanaut-cream/70">
                        {testimonial.role}
                      </div>
                    </footer>
                  </blockquote>
                </CardContent>
              </Card>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious className="border-atmanaut-olive/30 text-atmanaut-cream hover:bg-atmanaut-olive/20" />
        <CarouselNext className="border-atmanaut-olive/30 text-atmanaut-cream hover:bg-atmanaut-olive/20" />
      </Carousel>
    </div>
  );
};

export default TestimonialCarousel;
