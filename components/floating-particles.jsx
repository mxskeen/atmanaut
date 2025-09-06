"use client";

import React, { useEffect, useState } from "react";

const FloatingParticles = () => {
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const createParticle = () => ({
      id: Math.random(),
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      size: Math.random() * 4 + 1,
      speed: Math.random() * 0.5 + 0.1,
      opacity: Math.random() * 0.5 + 0.1,
    });

    const initialParticles = Array.from({ length: 20 }, createParticle);
    setParticles(initialParticles);

    const interval = setInterval(() => {
      setParticles((prev) =>
        prev
          .map((particle) => ({
            ...particle,
            y: particle.y - particle.speed,
            x: particle.x + Math.sin(particle.y * 0.01) * 0.5,
          }))
          .filter((particle) => particle.y > -50)
          .concat(Array.from({ length: 2 }, createParticle))
      );
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="absolute rounded-full bg-atmanaut-yellow/20 animate-zen-drift"
          style={{
            left: particle.x,
            top: particle.y,
            width: particle.size,
            height: particle.size,
            opacity: particle.opacity,
            animationDuration: `${8 + Math.random() * 4}s`,
          }}
        />
      ))}
    </div>
  );
};

export default FloatingParticles;
