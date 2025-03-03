import React, { useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";
import ControlButton from "../nextstepbutton/ControlButton";

function PlotlyCanvas({ point1, point2, draw }) {
  const [data, setData] = useState([{ x: [], y: [], mode: "lines+markers", type: "scatter" }]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [nextStep, setNextStep] = useState(false);
  const plotRef = useRef(null);

  // Используем рефы для хранения актуальных значений состояний
  const nextStepRef = useRef(nextStep);
  const isDrawingRef = useRef(isDrawing);

  useEffect(() => {
    nextStepRef.current = nextStep;
  }, [nextStep]);

  useEffect(() => {
    isDrawingRef.current = isDrawing;
  }, [isDrawing]);

  const drawPoint = async (x, y) => {
    setNextStep(false);
    setIsDrawing(true);

    await new Promise((resolve) => {
      const interval = setInterval(() => {
        if (nextStepRef.current) {
          clearInterval(interval);
          resolve();
        }
      }, 100);
    });

    setData((prevData) => {
      const newX = [...prevData[0].x, x];
      const newY = [...prevData[0].y, y];
      return [{ x: newX, y: newY, mode: "lines+markers", type: "scatter" }];
    });

    console.log(`(${x},${y})`)

    setIsDrawing(false);
  };

  const onNextStepClick = () => {
    if (isDrawingRef.current) {
      setNextStep(true);
    }
  };

  useEffect(() => {
    draw(point1, point2, drawPoint);
  }, []);

  return (
    <>
      <div style={{ padding: "25px", textAlign: "left" }}>
        <Plot
          ref={plotRef}
          data={data}
          layout={{
            title: "Координатная плоскость",
            xaxis: { title: "Ось X", range: [0, point2.x] },
            yaxis: { title: "Ось Y", range: [0, point2.y] },
            width: 500,
            height: 500,
            transition: { duration: 500, easing: "cubic-in-out" },
          }}
        />
        <ControlButton onClick={onNextStepClick} />
      </div>
    </>
  );
}

export default PlotlyCanvas;
