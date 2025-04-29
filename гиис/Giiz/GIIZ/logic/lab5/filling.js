import { pointInPolygon } from "./polygon";

const BOUNDS = { xMin: 0, xMax: 10, yMin: 0, yMax: 10 };

export const orderedEdgeListFill = (polygon) => {
  const edges = [];
  const steps = [];
  const filledPixels = [];

  // Генерация ребер с фильтрацией горизонтальных
  for (let i = 0; i < polygon.length; i++) {
    const p1 = polygon[i];
    const p2 = polygon[(i + 1) % polygon.length];
    
    if (Math.abs(p1.y - p2.y) < 1e-6) continue;

    const yMin = Math.min(p1.y, p2.y);
    const yMax = Math.max(p1.y, p2.y);
    const dx = (p2.x - p1.x) / (p2.y - p1.y);
    const x = p1.y === yMin ? p1.x : p2.x;

    edges.push({ yMin, yMax, x, dx });
  }

  edges.sort((a, b) => a.yMin - b.yMin);
  
  let activeEdges = [];
  let currentY = edges[0]?.yMin ?? 0;

  while (currentY <= BOUNDS.yMax && (activeEdges.length > 0 || edges.length > 0)) {
    // Добавление новых ребер
    while (edges.length > 0 && edges[0].yMin <= currentY) {
      activeEdges.push(edges.shift());
    }

    // Фильтрация и сортировка
    activeEdges = activeEdges.filter(ae => currentY < ae.yMax);
    activeEdges.sort((a, b) => a.x - b.x);

    // Закрашивание между ребрами
    for (let i = 0; i < activeEdges.length; i += 2) {
      const left = activeEdges[i];
      const right = activeEdges[i + 1];
      
      if (!right) break;

      const xStart = Math.max(BOUNDS.xMin, Math.ceil(left.x));
      const xEnd = Math.min(BOUNDS.xMax, Math.floor(right.x));

      if (xStart <= xEnd) {
        for (let x = xStart; x <= xEnd; x++) {
          filledPixels.push({ x, y: currentY });
          steps.push([...filledPixels]);
        }
      }
    }

    // Обновление координат
    activeEdges.forEach(ae => ae.x += ae.dx);
    currentY++;
  }

  return { filledPixels, steps };
};

export const activeEdgeListFill = (polygon) => {
  const edges = [];
  const steps = [];
  const filledPixels = [];

  // Инициализация ребер
  polygon.forEach((p1, i) => {
    const p2 = polygon[(i + 1) % polygon.length];
    if (Math.abs(p1.y - p2.y) < 1e-6) return;

    const yMin = Math.min(p1.y, p2.y);
    const yMax = Math.max(p1.y, p2.y);
    const dx = (p2.x - p1.x) / (p2.y - p1.y);
    const x = p1.y === yMin ? p1.x : p2.x;

    edges.push({ yMin, yMax, x, dx });
  });

  let y = Math.floor(Math.max(BOUNDS.yMin, Math.min(...polygon.map(p => p.y))));
  const maxY = Math.min(BOUNDS.yMax, Math.max(...polygon.map(p => p.y)));

  const activeEdges = [];
  
  while (y <= maxY) {
    // Обновление активных ребер
    edges.forEach(edge => {
      if (Math.floor(edge.yMin) === y) activeEdges.push({ ...edge });
    });

    activeEdges.sort((a, b) => a.x - b.x);
    
    // Удаление завершенных
    for (let i = activeEdges.length - 1; i >= 0; i--) {
      if (y >= activeEdges[i].yMax) activeEdges.splice(i, 1);
    }

    // Закрашивание
    for (let i = 0; i < activeEdges.length; i += 2) {
      const left = activeEdges[i];
      const right = activeEdges[i + 1] || left;
      
      const xStart = Math.max(BOUNDS.xMin, Math.ceil(left.x));
      const xEnd = Math.min(BOUNDS.xMax, Math.floor(right.x));

      if (xStart <= xEnd) {
        for (let x = xStart; x <= xEnd; x++) {
          filledPixels.push({ x, y });
          steps.push([...filledPixels]);
        }
      }
    }

    // Обновление X
    activeEdges.forEach(ae => ae.x += ae.dx);
    y++;
  }

  return { filledPixels, steps };
};

export const simpleSeedFill = (polygon, seed) => {
  const filledPixels = [];
  const steps = [];
  const stack = [];
  const visited = new Set();
  const getKey = (x, y) => `${x}|${y}`;

  // Валидация затравки
  if (!pointInPolygon(seed, polygon)) {
    throw new Error("Seed point outside polygon");
  }

  stack.push({ 
    x: Math.min(BOUNDS.xMax, Math.max(BOUNDS.xMin, Math.round(seed.x))),
    y: Math.min(BOUNDS.yMax, Math.max(BOUNDS.yMin, Math.round(seed.y)))
  });

  while (stack.length > 0) {
    const { x, y } = stack.pop();
    const key = getKey(x, y);

    if (visited.has(key) || !pointInPolygon({ x, y }, polygon)) continue;

    filledPixels.push({ x, y });
    steps.push([...filledPixels]);
    visited.add(key);

    // Добавление соседей с проверкой границ
    [
      { x: x + 1, y },
      { x: x - 1, y },
      { x, y: y + 1 },
      { x, y: y - 1 }
    ].forEach(({ x, y }) => {
      if (x >= BOUNDS.xMin && x <= BOUNDS.xMax && y >= BOUNDS.yMin && y <= BOUNDS.yMax) {
        stack.push({ x, y });
      }
    });
  }

  return { filledPixels, steps };
};

export const scanlineSeedFill = (polygon, seed) => {
  const filledPixels = [];
  const steps = [];
  const stack = [];
  const visited = new Set();
  const getKey = (x, y) => `${x}|${y}`;

  // Проверка валидности затравки
  if (!pointInPolygon(seed, polygon)) {
    throw new Error("Seed point outside polygon");
  }

  stack.push({
    x: Math.round(seed.x),
    y: Math.round(seed.y)
  });

  while (stack.length > 0) {
    const { x, y } = stack.pop();
    let left = x;
    let right = x;

    // Поиск границ с ограничениями
    while (left >= BOUNDS.xMin && pointInPolygon({ x: left - 1, y }, polygon)) left--;
    while (right <= BOUNDS.xMax && pointInPolygon({ x: right + 1, y }, polygon)) right++;

    // Закрашивание строки
    for (let px = left; px <= right; px++) {
      const key = getKey(px, y);
      
      if (!visited.has(key)) {
        filledPixels.push({ x: px, y });
        steps.push([...filledPixels]);
        visited.add(key);
      }
    }

    // Поиск новых затравок
    const checkLine = (ny) => {
      if (ny < BOUNDS.yMin || ny > BOUNDS.yMax) return;
      
      let inSegment = false;
      for (let px = left; px <= right; px++) {
        const inside = pointInPolygon({ x: px, y: ny }, polygon);
        
        if (!inSegment && inside) {
          const key = getKey(px, ny);
          if (!visited.has(key)) {
            stack.push({ x: px, y: ny });
            inSegment = true;
          }
        } else if (inSegment && !inside) {
          inSegment = false;
        }
      }
    };

    checkLine(y + 1);
    checkLine(y - 1);
  }

  return { filledPixels, steps };
};