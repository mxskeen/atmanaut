"use client";

import React from "react";

const ZenMeditationCircle = ({ size = "large", className = "" }) => {
  const sizeClasses = {
    small: "w-16 h-16",
    medium: "w-24 h-24",
    large: "w-32 h-32",
    xl: "w-40 h-40",
  };

  return (
    <div
      className={`${sizeClasses[size]} ${className} relative flex items-center justify-center`}
    >
      {/* Outer ring */}
      <div className="absolute inset-0 rounded-full border-2 border-atmanaut-yellow/30 animate-zen-rotate"></div>

      {/* Middle ring */}
      <div className="absolute inset-2 rounded-full border border-atmanaut-olive/40 animate-zen-pulse"></div>

      {/* Inner circle */}
      <div className="absolute inset-4 rounded-full bg-gradient-to-br from-atmanaut-yellow/20 to-atmanaut-cream/10 animate-zen-breathe"></div>

      {/* Center dot */}
      <div className="w-2 h-2 rounded-full bg-atmanaut-yellow animate-zen-glow"></div>
    </div>
  );
};

export default ZenMeditationCircle;
