import React, { useState, useRef } from "react";
import Plot from "react-plotly.js";
import { grahamScan, isConvex } from "../../logic/lab5/polygon";

const Transform2D = () => {
  const [originalPoints, setOriginalPoints] = useState([]);
  const [hullPoints, setHullPoints] = useState([]);
  const [inputCoords, setInputCoords] = useState({ x: "", y: "" });
  const [polygonType, setPolygonType] = useState("convex");
  const [status, setStatus] = useState("");
  const plotRef = useRef(null);

  const handleAddPoint = () => {
    const x = parseFloat(inputCoords.x);
    const y = parseFloat(inputCoords.y);
    
    if (isNaN(x) || isNaN(y) || x < 0 || x > 10 || y < 0 || y > 10) {
      setStatus("Ошибка: координаты от 0 до 10");
      return;
    }

    setOriginalPoints(prev => [...prev, { x, y }]);
    setInputCoords({ x: "", y: "" });
    setStatus(`Точка (${x.toFixed(1)}, ${y.toFixed(1)}) добавлена`);
  };

  const buildPolygon = () => {
    if (originalPoints.length < 3) {
      setStatus("Нужно минимум 3 точки!");
      return;
    }

    if (polygonType === "convex") {
      const hull = grahamScan(originalPoints);
      setHullPoints(hull);
      setStatus("Выпуклая оболочка построена");
    } else {
      setHullPoints([...originalPoints]);
      setStatus("Вогнутый полигон построен");
    }
  };

  const cohenSutherlandClip = () => {
    if (hullPoints.length < 3) return;

    const INSIDE = 0, LEFT = 1, RIGHT = 2, BOTTOM = 4, TOP = 8;
    const clipWindow = { x1: 2, y1: 2, x2: 8, y2: 8 };

    const computeCode = (x, y) => {
      let code = INSIDE;
      if (x < clipWindow.x1) code |= LEFT;
      else if (x > clipWindow.x2) code |= RIGHT;
      if (y < clipWindow.y1) code |= BOTTOM;
      else if (y > clipWindow.y2) code |= TOP;
      return code;
    };

    const newPoints = [];
    for (let i = 0; i < hullPoints.length; i++) {
      const p1 = hullPoints[i];
      const p2 = hullPoints[(i + 1) % hullPoints.length];
      
      let code1 = computeCode(p1.x, p1.y);
      let code2 = computeCode(p2.x, p2.y);
      let accept = false;

      while (true) {
        if (!(code1 | code2)) {
          accept = true;
          break;
        } else if (code1 & code2) break;
        else {
          let [x, y] = [0, 0];
          const codeOut = code1 || code2;

          if (codeOut & TOP) {
            x = p1.x + (p2.x - p1.x) * (clipWindow.y2 - p1.y) / (p2.y - p1.y);
            y = clipWindow.y2;
          } else if (codeOut & BOTTOM) {
            x = p1.x + (p2.x - p1.x) * (clipWindow.y1 - p1.y) / (p2.y - p1.y);
            y = clipWindow.y1;
          } else if (codeOut & RIGHT) {
            y = p1.y + (p2.y - p1.y) * (clipWindow.x2 - p1.x) / (p2.x - p1.x);
            x = clipWindow.x2;
          } else if (codeOut & LEFT) {
            y = p1.y + (p2.y - p1.y) * (clipWindow.x1 - p1.x) / (p2.x - p1.x);
            x = clipWindow.x1;
          }

          if (codeOut === code1) {
            p1.x = x;
            p1.y = y;
            code1 = computeCode(x, y);
          } else {
            p2.x = x;
            p2.y = y;
            code2 = computeCode(x, y);
          }
        }
      }
      if (accept) {
        newPoints.push(p1);
        newPoints.push(p2);
      }
    }
    
    setHullPoints(newPoints);
    setStatus("Отсечение выполнено");
  };

  const generatePlotData = () => {
    const clipWindow = { x1: 2, y1: 2, x2: 8, y2: 8 };

    return [
      {
        x: originalPoints.map(p => p.x),
        y: originalPoints.map(p => p.y),
        mode: "markers",
        type: "scatter",
        name: "Исходные точки",
        marker: { size: 12, color: "#ff0000" }
      },
      {
        x: [...hullPoints.map(p => p.x), hullPoints[0]?.x],
        y: [...hullPoints.map(p => p.y), hullPoints[0]?.y],
        mode: "lines+markers",
        type: "scatter",
        name: "Полигон",
        line: { color: polygonType === "convex" ? "#2196F3" : "#FF5722", width: 3 }
      },
      {
        x: [clipWindow.x1, clipWindow.x2, clipWindow.x2, clipWindow.x1, clipWindow.x1],
        y: [clipWindow.y1, clipWindow.y1, clipWindow.y2, clipWindow.y2, clipWindow.y1],
        mode: "lines",
        type: "scatter",
        name: "Окно отсечения",
        line: { color: "#00ff00", dash: "dot" }
      }
    ];
  };

  return (
    <div style={{ padding: 20 }}>
      <Plot
        ref={plotRef}
        data={generatePlotData()}
        layout={{
          width: 600,
          height: 400,
          title: "2D Отсечение полигонов",
          xaxis: { range: [0, 10] },
          yaxis: { range: [0, 10], scaleanchor: "x" }
        }}
        config={{ displayModeBar: false }}
      />

      <div style={{ marginTop: 20, display: "flex", flexWrap: "wrap", gap: 10 }}>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <input
            type="number"
            step="0.1"
            min="0"
            max="10"
            placeholder="X (0-10)"
            value={inputCoords.x}
            onChange={e => setInputCoords(p => ({...p, x: e.target.value}))}
            style={{ width: 100, padding: "5px" }}
          />
          <input
            type="number"
            step="0.1"
            min="0"
            max="10"
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

        <select
          value={polygonType}
          onChange={(e) => setPolygonType(e.target.value)}
          style={{ padding: "8px 16px", borderRadius: 4 }}
        >
          <option value="convex">Выпуклый</option>
          <option value="concave">Вогнутый</option>
        </select>

        <button
          onClick={buildPolygon}
          style={{ background: "#2196F3", color: "white", padding: "8px 16px" }}
        >
          Построить полигон
        </button>

        <button
          onClick={cohenSutherlandClip}
          style={{ background: "#E91E63", color: "white", padding: "8px 16px" }}
        >
          Отсечь
        </button>

        <button
          onClick={() => {
            setOriginalPoints([]);
            setHullPoints([]);
          }}
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
        borderRadius: 5,
        minHeight: 40
      }}>
        {status || "Готово к работе..."}
      </div>
    </div>
  );
};

export default Transform2D;