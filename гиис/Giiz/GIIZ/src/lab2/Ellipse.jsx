import React, { useRef, useEffect, useState } from "react";
import ControlButton from "../base/nextstepbutton/ControlButton";
import PixelPlot from "../base/plot/PixelPlot";

function Ellipse({ a, b, draw }) {
  const [pixelData, setPixelData] = useState(
    Array.from({ length:  a > b ? 2*a + 5 : 2*b + 5}, () => Array.from({ length: a > b ? 2*a + 5 : 2*b + 5}, () => 0))
  );
  const [isDrawing, setIsDrawing] = useState(false);
  const [nextStep, setNextStep] = useState(false);
  const [canSkip, setCanSkip] = useState(false);

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

  const drawPoint = async (x, y, intensity = 1) => {
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

    console.log(`${Math.floor(x)}, ${Math.floor(y)}`)

    setPixelData((prevData) => {
      const newData = prevData.map(row => [...row]); // Копируем предыдущие данные
      newData[Math.floor((a > b ? 2*a + 5 : 2*b + 5)/2) + Math.floor(y)][Math.floor((a > b ? 2*a + 5 : 2*b + 5)/2) + Math.floor(x)] = intensity; // Обновляем интенсивность пикселя
      return newData;
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
    draw(a, b, drawPoint);
  }, []);

  return (
    <>
      <div style={{ padding: "25px", textAlign: "left" }}>
        <PixelPlot
          width={a > b ? 2*a + 5 : 2*b + 5}
          height={a > b ? 2*a + 5 : 2*b + 5}
          pixelData={pixelData}
          isAutoSize={true}
        />
        <div style={{margin: "25px"}}>
          <ControlButton text={'Next step'} onClick={onNextStepClick} />
          <ControlButton text={'Skip'} onClick={onSkipClick} />
        </div>
      </div>
    </>
  );
}

export default Ellipse;
