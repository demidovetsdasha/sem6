import React, { useState, useRef } from "react";
import Plot from "react-plotly.js";
import { Delaunay } from "d3-delaunay";

function VoronoiDelaunay() {
  const [points, setPoints] = useState([]);
  const [mode, setMode] = useState("delaunay");
  const [status, setStatus] = useState("");
  const [inputCoords, setInputCoords] = useState({ x: "", y: "" });
  const plotRef = useRef(null);

  const handleAddPoint = () => {
    const x = parseFloat(inputCoords.x);
    const y = parseFloat(inputCoords.y);
    
    if (isNaN(x) || isNaN(y) || x < 0 || x > 10 || y < 0 || y > 10) {
      setStatus("Ошибка: координаты от 0 до 10");
      return;
    }

    setPoints(prev => [...prev, [x, y]]);
    setInputCoords({ x: "", y: "" });
    setStatus(`Добавлена точка (${x.toFixed(1)}, ${y.toFixed(1)})`);
  };

  const generateDelaunay = () => {
    if (points.length < 3) {
      setStatus("Нужно минимум 3 точки!");
      return;
    }
    setStatus("Триангуляция Делоне построена");
  };

  const generateVoronoi = () => {
    if (points.length < 3) {
      setStatus("Нужно минимум 3 точки!");
      return;
    }
    setStatus("Диаграмма Вороного построена");
  };

  const generatePlotData = () => {
    // Базовые данные с точками
    const baseData = [
      {
        x: points.map(p => p[0]),
        y: points.map(p => p[1]),
        mode: "markers",
        type: "scatter",
        name: "Точки",
        marker: { 
          size: 10, 
          color: "#ff0000",
          line: { width: 1, color: "black" }
        }
      }
    ];
  
    if (points.length < 3) return baseData;
  
    try {
      const delaunay = Delaunay.from(points);
      const voronoi = delaunay.voronoi([0, 0, 10, 10]);
  
      // Генерация триангуляции Делоне
      const delaunayLines = [];
      for (let i = 0; i < delaunay.triangles.length; i += 3) {
        const idx1 = delaunay.triangles[i];
        const idx2 = delaunay.triangles[i + 1];
        const idx3 = delaunay.triangles[i + 2];
  
        if (
          idx1 >= points.length ||
          idx2 >= points.length ||
          idx3 >= points.length
        ) continue;
  
        const p1 = points[idx1];
        const p2 = points[idx2];
        const p3 = points[idx3];
  
        if (!p1 || !p2 || !p3) continue;
  
        delaunayLines.push({
          x: [p1[0], p2[0], p3[0], p1[0]],
          y: [p1[1], p2[1], p3[1], p1[1]],
          mode: "lines",
          type: "scatter",
          line: { 
            color: "#2196F3", 
            width: 1.5,
            dash: "dot" 
          },
          hoverinfo: "none"
        });
      }
  
      // Генерация диаграммы Вороного
      const voronoiCells = [];
      for (let i = 0; i < points.length; i++) {
        try {
          const cell = voronoi.cellPolygon(i);
          if (cell && cell.length > 0) {
            const closedCell = [...cell, cell[0]]; // Замыкаем полигон
            voronoiCells.push({
              x: closedCell.map(p => p[0]),
              y: closedCell.map(p => p[1]),
              mode: "lines",
              type: "scatter",
              fill: "toself",
              line: { 
                color: "#FF5722", 
                width: 1 
              },
              opacity: 0.4,
              hoverinfo: "none"
            });
          }
        } catch (e) {
          console.warn(`Ошибка в ячейке ${i}:`, e);
        }
      }
  
      return [
        ...baseData,
        ...(mode === "delaunay" ? delaunayLines : []),
        ...(mode === "voronoi" ? voronoiCells : [])
      ];
  
    } catch (error) {
      console.error("Ошибка генерации:", error);
      return baseData;
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <Plot
        ref={plotRef}
        data={generatePlotData()}
        layout={{
          width: 800,
          height: 400,
          title: mode === "delaunay" 
            ? "Триангуляция Делоне" 
            : "Диаграмма Вороного",
          xaxis: { range: [0, 10], fixedrange: true },
          yaxis: { range: [0, 10], scaleanchor: "x" },
          showlegend: false
        }}
      />

      <div style={{ marginTop: 20, display: "flex", gap: 10, flexWrap: "wrap" }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <input
            type="number"
            step="0.1"
            placeholder="X (0-10)"
            value={inputCoords.x}
            onChange={e => setInputCoords(p => ({...p, x: e.target.value}))}
            style={{ width: 100, padding: "5px" }}
          />
          <input
            type="number"
            step="0.1"
            placeholder="Y (0-10)"
            value={inputCoords.y}
            onChange={e => setInputCoords(p => ({...p, y: e.target.value}))}
            style={{ width: 100, padding: "5px" }}
          />
          <button 
            onClick={handleAddPoint}
            style={{ background: "#4CAF50", color: "white", padding: "8px 16px" }}
          >
            Добавить
          </button>
        </div>

        <button
          onClick={() => setMode("delaunay")}
          style={{ 
            background: mode === "delaunay" ? "#2196F3" : "#ddd",
            color: "white",
            padding: "8px 16px"
          }}
        >
          Делоне
        </button>

        <button
          onClick={() => setMode("voronoi")}
          style={{ 
            background: mode === "voronoi" ? "#FF5722" : "#ddd",
            color: "white",
            padding: "8px 16px"
          }}
        >
          Вороного
        </button>

        <button
          onClick={() => setPoints([])}
          style={{ background: "#f44336", color: "white", padding: "8px 16px" }}
        >
          Очистить
        </button>
      </div>

      <div style={{ 
        marginTop: 15,
        padding: 10,
        color: "black",
        background: "#f8f9fa",
        borderRadius: 5
      }}>
        {status || "Добавьте точки и выберите режим"}
      </div>
    </div>
  );
}

export default VoronoiDelaunay;