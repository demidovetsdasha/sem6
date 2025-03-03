import React, { useRef, useEffect, useState } from "react";
import Plot from "react-plotly.js";
import ControlButton from "../base/nextstepbutton/ControlButton";

function Bezier({ p, draw }) {
      const [data, setData] = useState([{ x: [], y: [], mode: "lines+markers", type: "scatter" }]);
      const [isDrawing, setIsDrawing] = useState(false);
      const [nextStep, setNextStep] = useState(false);
      const [canSkip, setCanSkip] = useState(false);
      const plotRef = useRef(null);
    
      // Используем рефы для хранения актуальных значений состояний
      const nextStepRef = useRef(nextStep);
      const isDrawingRef = useRef(isDrawing);
      const canSkipRef = useRef(canSkip)
    
      useEffect(() => {
        nextStepRef.current = nextStep;
      }, [nextStep]);
    
      useEffect(() => {
        isDrawingRef.current = isDrawing;
      }, [isDrawing]);
    
      useEffect(() => {
          canSkipRef.current = canSkip
        }, [canSkip])
    
      const drawPoint = async (x, y) => {
          if(canSkipRef.current === false) {
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
          }
          else {
            await new Promise(resolve => setTimeout(resolve, 100));
          }
      
          setData((prevData) => {
            const newX = [...prevData[0].x, x];
            const newY = [...prevData[0].y, y];
            return [{ x: newX, y: newY, mode: "lines+markers", type: "scatter" }];
          });
      
          console.log(`(${x},${y})`)
      
          if(canSkip === false)
            setIsDrawing(false);
      };
  
    const onNextStepClick = () => {
      if (isDrawingRef.current) {
        setNextStep(true);
      }
    };
  
    const onSkipClick = () => {
      setCanSkip(true)
  
      console.log(canSkip)
    };

  useEffect(() => {
    draw(p, drawPoint);
  }, []);

  return (
    <>
      <div style={{ padding: "25px", textAlign: "left" }}>
        <Plot
          ref={plotRef}
          data={data}
          layout={{
            title: "Координатная плоскость",
            xaxis: { title: "Ось X", range: [0, 10] },
            yaxis: { title: "Ось Y", range: [0, 10] },
            width: 500,
            height: 500,
            transition: { duration: 500, easing: "cubic-in-out" },
          }}
        />
        <div>
          <ControlButton text={'Next step'} onClick={onNextStepClick} />
          <ControlButton text={'Skip'} onClick={onSkipClick} />
        </div>
      </div>
    </>
  );
}

export default Bezier;
