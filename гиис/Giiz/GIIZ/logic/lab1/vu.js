export async function draw(point1, point2, drawPoint) {
    let x0 = point1.x;
    let y0 = point1.y;
    let x1 = point2.x;
    let y1 = point2.y;

    const steep = Math.abs(y1 - y0) > Math.abs(x1 - x0);

    // Если линия крутая - меняем местами x и y
    if (steep) {
        [x0, y0] = [y0, x0];
        [x1, y1] = [y1, x1];
    }

    // Всегда рисуем слева направо
    if (x0 > x1) {
        [x0, x1] = [x1, x0];
        [y0, y1] = [y1, y0];
    }

    const dx = x1 - x0;
    const dy = y1 - y0;
    const gradient = dx === 0 ? 1 : dy / dx; // Защита от деления на 0

    let y = y0;

    for (let x = x0; x <= x1; x++) {
        // Корректный расчет координаты Y
        const yend = y0 + gradient * (x - x0); // Исправлено!
        const yfrac = yend - Math.floor(yend);

        // Основной пиксель
        const xpx1 = steep ? Math.floor(yend) : x;
        const ypx1 = steep ? x : Math.floor(yend);

        // Соседний пиксель (сверху или снизу)
        const xpx2 = steep ? Math.floor(yend) + 1 : x;
        const ypx2 = steep ? x : Math.floor(yend) + 1;

        // Интенсивности
        const intensity1 = 1 - yfrac;
        const intensity2 = yfrac;

        // Рисуем оба пикселя
        await drawPoint(xpx1, ypx1, intensity1);
        await drawPoint(xpx2, ypx2, intensity2);

        y += gradient;
    }
}