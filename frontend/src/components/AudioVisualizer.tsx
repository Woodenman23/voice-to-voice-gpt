import React, { useRef, useEffect } from 'react';

interface AudioVisualizerProps {
  isActive: boolean;
}

const AudioVisualizer: React.FC<AudioVisualizerProps> = ({ isActive }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<number | undefined>();

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;

    let frame = 0;

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      if (isActive) {
        // AI is speaking - animated visualization
        const time = frame * 0.1;
        const radius = 50 + Math.sin(time) * 20;
        const pulse = Math.sin(time * 2) * 0.3 + 0.7;

        // Main pulsing circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(74, 144, 226, ${pulse})`;
        ctx.fill();

        // Outer ring
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius + 20, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(74, 144, 226, ${pulse * 0.5})`;
        ctx.lineWidth = 3;
        ctx.stroke();

        // Animated bars around the circle
        const numBars = 12;
        for (let i = 0; i < numBars; i++) {
          const angle = (i / numBars) * Math.PI * 2;
          const barHeight = 20 + Math.sin(time + i) * 15;
          const x1 = centerX + Math.cos(angle) * (radius + 30);
          const y1 = centerY + Math.sin(angle) * (radius + 30);
          const x2 = centerX + Math.cos(angle) * (radius + 30 + barHeight);
          const y2 = centerY + Math.sin(angle) * (radius + 30 + barHeight);

          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.strokeStyle = `rgba(74, 144, 226, ${pulse})`;
          ctx.lineWidth = 4;
          ctx.stroke();
        }
      } else {
        // AI is idle - static gentle glow
        ctx.beginPath();
        ctx.arc(centerX, centerY, 30, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(74, 144, 226, 0.3)';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(centerX, centerY, 30, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(74, 144, 226, 0.5)';
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      frame++;
      animationRef.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isActive]);

  return (
    <div className="audio-visualizer">
      <canvas
        ref={canvasRef}
        width={400}
        height={400}
        style={{
          border: '1px solid #333',
          borderRadius: '10px',
          backgroundColor: '#000'
        }}
      />
    </div>
  );
};

export default AudioVisualizer;