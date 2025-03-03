import React from 'react';

function PixelPlot({ width, height, pixelData }) {
  const pixelSize = 35; // Размер каждого пикселя в пикселях

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${width}, ${pixelSize}px)`,
        gridTemplateRows: `repeat(${height}, ${pixelSize}px)`,
        gap: '1px',
      }}
    >
      {pixelData.map((row, y) =>
        row.map((intensity, x) => (
          <div
            key={`${x}-${y}`}
            style={{
              width: pixelSize,
              height: pixelSize,
              backgroundColor: `rgba(0, 0, 0, ${intensity})`,
              border: '1px solid #ddd',
            }}
          />
        ))
      ).reverse()} {/* Инвертируем строки, чтобы y = 0 был внизу */}
    </div>
  );
};

export default PixelPlot;