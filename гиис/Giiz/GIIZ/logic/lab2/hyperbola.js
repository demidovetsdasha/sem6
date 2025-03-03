export async function draw(a, b, drawPoint) {
    // Начальная точка - пересечение с осью X
    let x = Math.ceil(a);  // Округляем в большую сторону для целых координат
    let y = 0;
    
    // Начальное значение дельта-параметра
    let delta = b * b + a;
    
    // Ограничение по оси X (15 пикселей)
    let limitX = 13;
    let limitY = 13;
    
    // Функция проверки близости точки к гиперболе
    function checkPoint(x, y) {
        return Math.abs((x * x / (a * a)) - (y * y / (b * b)) - 1);
    }
    
    await drawPoint(x, y);
    await drawPoint(-x, y);
    await drawPoint(x, -y);
    await drawPoint(-x, -y); // Рисуем начальную точку
    
    while (x <= limitX && y <= limitY) {
        // Вычисляем три потенциальные следующей точки
        const points = [
            {x: x + 1, y: y},           // Только x
            {x: x + 1, y: y + 1},       // x и y
            {x: x + 1, y: y + 2}        // x и y+1
        ];
        
        // Находим точку, наиболее близкую к гиперболе
        const distances = points.map(p => checkPoint(p.x, p.y));
        const minDistIndex = distances.indexOf(Math.min(...distances));
        
        // Выбираем точку с минимальным отклонением от гиперболы
        const nextPoint = points[minDistIndex];
        x = nextPoint.x;
        y = nextPoint.y;
        
        await drawPoint(x, y);
        await drawPoint(-x, y);
        await drawPoint(x, -y);
        await drawPoint(-x, -y);
    }
}