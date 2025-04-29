export function isConvex(points) {
    if (points.length < 3) return false;
    let prevCross = 0;
    
    for (let i = 0; i < points.length; i++) {
        const p1 = points[i];
        const p2 = points[(i + 1) % points.length];
        const p3 = points[(i + 2) % points.length];

        const dx1 = p2.x - p1.x;
        const dy1 = p2.y - p1.y;
        const dx2 = p3.x - p2.x;
        const dy2 = p3.y - p2.y;
        
        const cross = dx1 * dy2 - dy1 * dx2;
        
        if (cross !== 0) {
            if (cross * prevCross < 0) return false;
            prevCross = cross;
        }
    }
    return true;
}

export function grahamScan(points) {
    if (points.length < 3) return points;

    // Шаг 1: Найти опорную точку с минимальными y и x
    const pivot = points.reduce((min, p) => 
        p.y < min.y || (p.y === min.y && p.x < min.x) ? p : min
    );

    // Шаг 2: Сортировка по полярному углу и расстоянию
    const sorted = [...points].sort((a, b) => {
        const angleA = Math.atan2(a.y - pivot.y, a.x - pivot.x);
        const angleB = Math.atan2(b.y - pivot.y, b.x - pivot.x);

        if (angleA !== angleB) return angleA - angleB;
        return (a.x - pivot.x) ** 2 + (a.y - pivot.y) ** 2 - 
               ((b.x - pivot.x) ** 2 + (b.y - pivot.y) ** 2);
    });

    // Шаг 3: Построение выпуклой оболочки
    const hull = [sorted[0], sorted[1]];
    for (let i = 2; i < sorted.length; i++) {
        while (hull.length > 1) {
            const a = hull[hull.length - 2];
            const b = hull[hull.length - 1];
            const c = sorted[i];
            
            const cross = (b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x);
            
            // Если поворот направо или коллинеарны, удаляем последнюю точку
            if (cross <= 0) {
                hull.pop();
            } else {
                break;
            }
        }
        hull.push(sorted[i]);
    }

    return hull;
}

// Функция построения вогнутого полигона (просто соединяет точки линиями)
export function buildConcavePolygon(points) {
    if (points.length < 3) return [];
    return [...points, points[0]]; // Соединяем последнюю точку с первой
}


export function lineIntersection(line1, line2) {
    const x1 = line1.x1, y1 = line1.y1;
    const x2 = line1.x2, y2 = line1.y2;
    const x3 = line2.x1, y3 = line2.y1;
    const x4 = line2.x2, y4 = line2.y2;

    const denominator = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1);
    if (denominator === 0) return null;

    const ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator;
    const ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator;

    if (ua >= 0 && ua <= 1 && ub >= 0 && ub <= 1) {
        return {
            x: x1 + ua * (x2 - x1),
            y: y1 + ua * (y2 - y1)
        };
    }
    return null;
}
// Алгоритм Джарвиса
export function jarvisMarch(points) {
    if (points.length < 3) return points;
    
    const hull = [];
    let current = points.reduce((min, p) => p.x < min.x ? p : min);
    
    do {
        hull.push(current);
        let next = points[0];
        
        for (const p of points) {
            if (p === current) continue;
            const cross = (next.x - current.x) * (p.y - current.y) - 
                         (next.y - current.y) * (p.x - current.x);
            
            if (next === current || cross > 0 || 
                (cross === 0 && distance(current, p) > distance(current, next))) {
                next = p;
            }
        }
        current = next;
    } while (current !== hull[0]);
    
    return hull;
}

// Проверка принадлежности точки полигону (алгоритм луча)
export function pointInPolygon(point, polygon) {
    let inside = false;
    for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i].x, yi = polygon[i].y;
        const xj = polygon[j].x, yj = polygon[j].y;
        
        const intersect = ((yi > point.y) !== (yj > point.y)) &&
            (point.x < (xj - xi) * (point.y - yi) / (yj - yi) + xi);
        
        if (intersect) inside = !inside;
    }
    return inside;
}

// Нахождение нормалей
export function calculateNormals(polygon) {
    const normals = [];
    for (let i = 0; i < polygon.length; i++) {
        const p1 = polygon[i];
        const p2 = polygon[(i + 1) % polygon.length];
        
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        
        // Перпендикулярный вектор
        const normal = { x: -dy, y: dx };
        
        // Нормализуем и направляем внутрь
        const length = Math.sqrt(normal.x**2 + normal.y**2);
        normal.x /= length;
        normal.y /= length;
        
        // Проверяем направление
        const midPoint = { x: (p1.x + p2.x)/2, y: (p1.y + p2.y)/2 };
        const testPoint = { 
            x: midPoint.x + normal.x, 
            y: midPoint.y + normal.y 
        };
        
        if (!pointInPolygon(testPoint, polygon)) {
            normal.x *= -1;
            normal.y *= -1;
        }
        
        normals.push(normal);
    }
    return normals;
}

// Вспомогательные функции
function distance(a, b) {
    return Math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2);
}