"use client";

import React, { useState, useEffect, useRef } from "react";
import { Play, Pause, RotateCcw, Volume2, VolumeX } from "lucide-react";

const ZenBreathingGuide = () => {
  const [isActive, setIsActive] = useState(false);
  const [phase, setPhase] = useState("inhale"); // inhale, hold, exhale, pause
  const [count, setCount] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [isClient, setIsClient] = useState(false);
  const audioRef = useRef(null);

  const breathingCycle = [
    { phase: "inhale", duration: 4000, text: "Breathe In" },
    { phase: "hold", duration: 2000, text: "Hold" },
    { phase: "exhale", duration: 6000, text: "Breathe Out" },
    { phase: "pause", duration: 2000, text: "Rest" },
  ];

  useEffect(() => {
    setIsClient(true);
  }, []);

  useEffect(() => {
    if (!isActive || !isClient) return;

    const cycle = breathingCycle[count % breathingCycle.length];
    const timer = setTimeout(() => {
      setPhase(cycle.phase);
      setCount((prev) => prev + 1);
    }, cycle.duration);

    return () => clearTimeout(timer);
  }, [isActive, count, isClient]);

  useEffect(() => {
    if (audioRef.current && isClient) {
      if (isMuted) {
        audioRef.current.volume = 0;
      } else {
        audioRef.current.volume = 0.3;
      }
    }
  }, [isMuted, isClient]);

  const currentCycle = breathingCycle[count % breathingCycle.length];

  const handlePlayPause = () => {
    if (!isClient) return;

    setIsActive(!isActive);
    if (!isActive && audioRef.current) {
      audioRef.current.play().catch(console.error);
    } else if (audioRef.current) {
      audioRef.current.pause();
    }
  };

  const handleReset = () => {
    if (!isClient) return;

    setIsActive(false);
    setCount(0);
    setPhase("inhale");
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  return (
    <div className="cosmic-card p-8 rounded-2xl text-center animate-zen-fade-in relative overflow-hidden">
      {/* Audio element */}
      <audio ref={audioRef} loop>
        <source src="/cosmiczen.mp3" type="audio/mpeg" />
      </audio>

      {/* Cosmic background elements */}
      <div className="absolute inset-0 opacity-20 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-atmanaut-yellow rounded-full animate-flicker"></div>
        <div
          className="absolute top-1/3 right-1/3 w-1 h-1 bg-atmanaut-cream rounded-full animate-flicker"
          style={{ animationDelay: "1s" }}
        ></div>
        <div
          className="absolute bottom-1/4 left-1/2 w-1.5 h-1.5 bg-atmanaut-olive rounded-full animate-flicker"
          style={{ animationDelay: "2s" }}
        ></div>
        <div
          className="absolute bottom-1/3 left-1/5 w-1 h-1 bg-atmanaut-yellow rounded-full animate-flicker"
          style={{ animationDelay: "3s" }}
        ></div>
      </div>

      <h3 className="text-xl font-semibold text-atmanaut-cream mb-6 relative z-10">
        Play to Calm Your Nervous System
      </h3>

      <div className="relative mb-8">
        <div
          className={`w-32 h-32 mx-auto rounded-full border-4 border-atmanaut-yellow/40 transition-all duration-1000 cosmic-pulse ${
            phase === "inhale"
              ? "scale-110 cosmic-glow"
              : phase === "hold"
              ? "scale-110"
              : phase === "exhale"
              ? "scale-100"
              : "scale-90"
          }`}
        >
          <div className="absolute inset-4 rounded-full bg-gradient-to-br from-atmanaut-dark/30 via-atmanaut-yellow/20 to-atmanaut-cream/10"></div>
        </div>
      </div>

      <div className="mb-6 relative z-10">
        <p className="text-2xl font-bold text-atmanaut-yellow mb-2">
          {currentCycle.text}
        </p>
        <p className="text-atmanaut-cream/70">
          {phase === "inhale" && "Still your mind, breathe deeply"}
          {phase === "hold" && "Feel the calm energy within"}
          {phase === "exhale" && "Release stress and tension"}
          {phase === "pause" && "Find your center, find your peace"}
        </p>
      </div>

      <div className="flex justify-center gap-4 relative z-10">
        <button
          onClick={handlePlayPause}
          disabled={!isClient}
          className="p-3 rounded-full bg-atmanaut-yellow/20 text-atmanaut-cream hover:bg-atmanaut-yellow/30 transition-all duration-300 apple-hover-button disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isActive ? <Pause size={20} /> : <Play size={20} />}
        </button>

        <button
          onClick={handleReset}
          disabled={!isClient}
          className="p-3 rounded-full bg-atmanaut-olive/20 text-atmanaut-cream hover:bg-atmanaut-olive/30 transition-all duration-300 apple-hover-button disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RotateCcw size={20} />
        </button>

        <button
          onClick={() => setIsMuted(!isMuted)}
          disabled={!isClient}
          className="p-3 rounded-full bg-atmanaut-dark-olive/20 text-atmanaut-cream hover:bg-atmanaut-dark-olive/30 transition-all duration-300 apple-hover-button disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
        </button>
      </div>
    </div>
  );
};

export default ZenBreathingGuide;
