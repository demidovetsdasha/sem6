import React, { useState, useRef } from "react";
import Plot from "react-plotly.js";
import { 
  isConvex, 
  grahamScan, 
  jarvisMarch, 
  calculateNormals, 
  pointInPolygon,
  lineIntersection 
} from "../../logic/lab5/polygon";

function Polygon() {
  const [originalPoints, setOriginalPoints] = useState([]);
  const [hullPoints, setHullPoints] = useState([]);
  const [segments, setSegments] = useState([]);
  const [testPoint, setTestPoint] = useState(null);
  const [mode, setMode] = useState("polygon");
  const [convexHullMethod, setConvexHullMethod] = useState("graham");
  const [normals, setNormals] = useState([]);
  const [status, setStatus] = useState("");
  const [inputCoords, setInputCoords] = useState({ x: "", y: "" });
  const [intersections, setIntersections] = useState([]);
  const [polygonType, setPolygonType] = useState("convex");
  const plotRef = useRef(null);

  const handleAddPoint = () => {
    const x = parseFloat(inputCoords.x);
    const y = parseFloat(inputCoords.y);
    
    if (isNaN(x) || isNaN(y) || x < 0 || x > 10 || y < 0 || y > 10) {
      setStatus("Ошибка: введите координаты от 0 до 10");
      return;
    }

    const newPoint = { x, y };

    switch(mode) {
      case "polygon":
        setOriginalPoints(prev => [...prev, newPoint]);
        break;
      case "segment":
        setSegments(prev => [...prev, newPoint]);
        break;
      case "test":
        setTestPoint(newPoint);
        break;
      default:
        break;
    }

    setInputCoords({ x: "", y: "" });
    setStatus(`Точка (${x.toFixed(1)}, ${y.toFixed(1)}) добавлена`);
  };

  const calculateConvexHull = () => {
    if (polygonType === "concave") {
      setHullPoints([...originalPoints]);
      setStatus("Вогнутый полигон построен");
      return;
    }
    
    if (originalPoints.length < 3) {
      setStatus("Нужно минимум 3 точки!");
      return;
    }
    
    const hull = convexHullMethod === "graham" 
      ? grahamScan(originalPoints) 
      : jarvisMarch(originalPoints);
    setHullPoints(hull);
    setStatus(`Построена оболочка (${hull.length} точек)`);
  };

  const checkIntersections = () => {
    const results = [];
    for (let i = 0; i < segments.length; i += 2) {
      const start = segments[i];
      const end = segments[i + 1];
      if (!start || !end) continue;

      hullPoints.forEach((p1, j) => {
        const p2 = hullPoints[(j + 1) % hullPoints.length];
        const intersect = lineIntersection(
          { x1: start.x, y1: start.y, x2: end.x, y2: end.y },
          { x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y }
        );
        if (intersect) results.push(intersect);
      });
    }
    setIntersections(results);
    setStatus(`Найдено пересечений: ${results.length}`);
  };

  const generatePlotData = () => {
    const segmentLines = [];
    for (let i = 0; i < segments.length; i += 2) {
      const start = segments[i];
      const end = segments[i + 1];
      if (start && end) {
        segmentLines.push({
          x: [start.x, end.x],
          y: [start.y, end.y],
          mode: "lines+markers",
          type: "scatter",
          name: `Отрезок ${i/2 + 1}`,
          line: { color: "#00ff00", width: 2 }
        });
      }
    }

    const polygonColor = polygonType === "convex" ? "#2196F3" : "#FF5722";
    const polygonName = polygonType === "convex" ? "Выпуклая оболочка" : "Вогнутый полигон";

    return [
      {
        x: originalPoints.map(p => p.x),
        y: originalPoints.map(p => p.y),
        mode: "markers",
        type: "scatter",
        name: "Исходные точки",
        marker: { size: 12, color: "#ff0000" }
      },
      ...segmentLines,
      ...(hullPoints.length > 0 ? [{
        x: [...hullPoints.map(p => p.x), hullPoints[0].x],
        y: [...hullPoints.map(p => p.y), hullPoints[0].y],
        mode: "lines+markers",
        type: "scatter",
        name: polygonName,
        line: { color: polygonColor, width: 3 }
      }] : []),
      ...(testPoint ? [{
        x: [testPoint.x],
        y: [testPoint.y],
        mode: "markers",
        type: "scatter",
        name: "Тестовая точка",
        marker: { color: "#9C27B0", size: 16 }
      }] : []),
      ...normals.map((normal, i) => ({
        x: [hullPoints[i].x, hullPoints[i].x + normal.x],
        y: [hullPoints[i].y, hullPoints[i].y + normal.y],
        mode: "lines",
        type: "scatter",
        name: `Нормаль ${i + 1}`,
        line: { color: "#FF9800", width: 2 }
      })),
      ...intersections.map(p => ({
        x: [p.x],
        y: [p.y],
        mode: "markers",
        type: "scatter",
        name: "Пересечение",
        marker: { color: "#E91E63", size: 14 }
      }))
    ];
  };

  return (
    <div style={{ padding: 20 }}>
      <Plot
        ref={plotRef}
        data={generatePlotData()}
        layout={{
          width: 400,
          height: 400,
          title: "Графический редактор полигонов",
          xaxis: { range: [0, 10], fixedrange: true, zeroline: false },
          yaxis: { range: [0, 10], scaleanchor: "x", fixedrange: true },
          hovermode: "closest",
          dragmode: false
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
          value={mode}
          onChange={e => setMode(e.target.value)}
          style={{ padding: "8px 16px", borderRadius: 4 }}
        >
          <option value="polygon">Полигон</option>
          <option value="segment">Отрезок</option>
          <option value="test">Тест точки</option>
        </select>

        <select
          value={polygonType}
          onChange={(e) => setPolygonType(e.target.value)}
          style={{ padding: "8px 16px", borderRadius: 4 }}
        >
          <option value="convex">Выпуклый</option>
          <option value="concave">Вогнутый</option>
        </select>

        <select
          value={convexHullMethod}
          onChange={e => setConvexHullMethod(e.target.value)}
          style={{ padding: "8px 16px", borderRadius: 4 }}
          disabled={polygonType === "concave"}
        >
          <option value="graham">Грэхем</option>
          <option value="jarvis">Джарвис</option>
        </select>

        <button
          onClick={calculateConvexHull}
          style={{ 
            background: "#2196F3", 
            color: "white", 
            padding: "8px 16px",
            opacity: polygonType === "concave" ? 0.5 : 1
          }}
          disabled={polygonType === "concave"}
        >
          Построить оболочку
        </button>

        <button
          onClick={() => {
            if (hullPoints.length < 3) {
              setStatus("Сначала постройте оболочку!");
              return;
            }
            setNormals(calculateNormals(hullPoints));
            setStatus(`Оболочка ${isConvex(hullPoints) ? "выпуклая" : "не выпуклая"}`);
          }}
          style={{ background: "#FF9800", color: "white", padding: "8px 16px" }}
        >
          Нормали
        </button>

        <button
          onClick={checkIntersections}
          style={{ background: "#E91E63", color: "white", padding: "8px 16px" }}
        >
          Пересечения
        </button>

        {testPoint && (
          <button
            onClick={() => {
              const inside = pointInPolygon(testPoint, hullPoints);
              setStatus(inside ? "✅ Точка внутри" : "❌ Точка снаружи");
            }}
            style={{ background: "#9C27B0", color: "white", padding: "8px 16px" }}
          >
            Проверить точку
          </button>
        )}
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
}

export default Polygon;