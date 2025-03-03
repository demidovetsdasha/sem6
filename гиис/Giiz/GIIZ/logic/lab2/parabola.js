export async function draw(p, drawPoint) {
    // Начальная точка - начало координат
    let x = 0;
    let y = 0;
    
    // Ограничение по осям (15 пикселей)
    let limitX = 14;
    let limitY = 14;
    
    // Функция проверки близости точки к параболе
    function checkPoint(x, y) {
        return Math.abs((y * y / (2 * p)) - x);
    }

    await drawPoint(x, y);
    await drawPoint(x, -y); // Рисуем начальную точку
    
    while (x <= limitX && y <= limitY) {
        // Вычисляем три потенциальные следующей точки
        const points = [
            {x: x + 1, y: y},           // Только x
            {x: x + 1, y: y + 1},       // x и y
            {x: x + 1, y: y + 2}        // x и y+1
        ];
        
        // Находим точку, наиболее близкую к параболе
        const distances = points.map(p => checkPoint(p.x, p.y));
        const minDistIndex = distances.indexOf(Math.min(...distances));
        
        // Выбираем точку с минимальным отклонением от параболы
        const nextPoint = points[minDistIndex];
        x = nextPoint.x;
        y = nextPoint.y;
        
        await drawPoint(x, y);
        await drawPoint(x, -y);
    }
}