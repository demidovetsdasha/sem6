import React, { useState, useRef } from "react";
import Plot from "react-plotly.js";

const clipWindow = { xMin: 2, xMax: 8, yMin: 2, yMax: 8 };

const Transform2D = () => {
  const [points, setPoints] = useState([]);
  const [segments, setSegments] = useState([]);
  const [clippedSegments, setClippedSegments] = useState([]);
  const [inputCoords, setInputCoords] = useState({ x: "", y: "" });
  const [status, setStatus] = useState("Введите хотя бы 2 точки");
  const plotRef = useRef(null);

  const handleAddPoint = () => {
    const x = parseFloat(inputCoords.x);
    const y = parseFloat(inputCoords.y);
    if (isNaN(x) || isNaN(y) || x < 0 || x > 10 || y < 0 || y > 10) {
      setStatus("Ошибка: координаты должны быть в диапазоне [0, 10]");
      return;
    }

    const newPoints = [...points, { x, y }];
    setPoints(newPoints);
    setInputCoords({ x: "", y: "" });
    setStatus(`Точка (${x}, ${y}) добавлена`);

    if (newPoints.length >= 2) {
      const last = newPoints[newPoints.length - 2];
      setSegments((prev) => [...prev, { p1: last, p2: { x, y } }]);
    }
  };

  // Алгоритм Коэна-Сазерленда
  const getRegionCode = (p) => {
    let code = 0;
    if (p.x < clipWindow.xMin) code |= 1;
    if (p.x > clipWindow.xMax) code |= 2;
    if (p.y < clipWindow.yMin) code |= 4;
    if (p.y > clipWindow.yMax) code |= 8;
    return code;
  };

  const cohenSutherlandClip = (p1, p2) => {
    let code1 = getRegionCode(p1);
    let code2 = getRegionCode(p2);
    let accept = false;

    while (true) {
      if ((code1 | code2) === 0) {
        accept = true;
        break;
      } else if ((code1 & code2) !== 0) {
        break;
      } else {
        let x, y;
        const outCode = code1 ? code1 : code2;
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;

        if (outCode & 8) {
          x = p1.x + dx * (clipWindow.yMax - p1.y) / dy;
          y = clipWindow.yMax;
        } else if (outCode & 4) {
          x = p1.x + dx * (clipWindow.yMin - p1.y) / dy;
          y = clipWindow.yMin;
        } else if (outCode & 2) {
          y = p1.y + dy * (clipWindow.xMax - p1.x) / dx;
          x = clipWindow.xMax;
        } else if (outCode & 1) {
          y = p1.y + dy * (clipWindow.xMin - p1.x) / dx;
          x = clipWindow.xMin;
        }

        if (outCode === code1) {
          p1 = { x, y };
          code1 = getRegionCode(p1);
        } else {
          p2 = { x, y };
          code2 = getRegionCode(p2);
        }
      }
    }

    if (accept) return { p1, p2 };
    return null;
  };

  const clipAllSegments = () => {
    const clipped = [];
    for (const seg of segments) {
      const result = cohenSutherlandClip(seg.p1, seg.p2);
      if (result) clipped.push(result);
    }
    setClippedSegments(clipped);
    setStatus("Отсечение завершено");
  };

  const resetAll = () => {
    setPoints([]);
    setSegments([]);
    setClippedSegments([]);
    setInputCoords({ x: "", y: "" });
    setStatus("Очищено");
  };

  const generatePlotData = () => {
    const data = [];

    // Окно отсечения
    data.push({
      x: [clipWindow.xMin, clipWindow.xMax, clipWindow.xMax, clipWindow.xMin, clipWindow.xMin],
      y: [clipWindow.yMin, clipWindow.yMin, clipWindow.yMax, clipWindow.yMax, clipWindow.yMin],
      type: "scatter",
      mode: "lines",
      name: "Окно",
      line: { color: "green", dash: "dot" },
    });

    // Все отрезки
    segments.forEach((seg, idx) =>
      data.push({
        x: [seg.p1.x, seg.p2.x],
        y: [seg.p1.y, seg.p2.y],
        type: "scatter",
        mode: "lines+markers",
        name: `Отрезок ${idx + 1}`,
        line: { color: "red" },
        marker: { color: "red" },
      })
    );

    // Отсечённые отрезки
    clippedSegments.forEach((seg, idx) =>
      data.push({
        x: [seg.p1.x, seg.p2.x],
        y: [seg.p1.y, seg.p2.y],
        type: "scatter",
        mode: "lines",
        name: `Отсечённый ${idx + 1}`,
        line: { color: "blue", width: 4 },
      })
    );

    return data;
  };

  return (
    <div style={{ padding: 20 }}>
      <Plot
        ref={plotRef}
        data={generatePlotData()}
        layout={{
          width: 700,
          height: 500,
          title: "Отсечение отрезков",
          xaxis: { range: [0, 10] },
          yaxis: { range: [0, 10], scaleanchor: "x" },
        }}
      />

      <div style={{ marginTop: 20, display: "flex", gap: 10 }}>
        <input
          type="number"
          step="0.1"
          min="0"
          max="10"
          placeholder="X"
          value={inputCoords.x}
          onChange={(e) => setInputCoords((p) => ({ ...p, x: e.target.value }))}
        />
        <input
          type="number"
          step="0.1"
          min="0"
          max="10"
          placeholder="Y"
          value={inputCoords.y}
          onChange={(e) => setInputCoords((p) => ({ ...p, y: e.target.value }))}
        />
        <button onClick={handleAddPoint}>Добавить точку</button>
        <button onClick={clipAllSegments}>Отсечь</button>
        <button onClick={resetAll}>Сброс</button>
      </div>

      <div style={{ marginTop: 10, fontWeight: "bold" }}>{status}</div>
    </div>
  );
};

export default Transform2D;
