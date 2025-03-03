export async function draw(point1, point2, drawPoint) {
    let x = point1.x;
    let y = point1.y;

    let dx = point2.x - point1.x;
    let dy = point2.y - point1.y;

    let e = (2 * dy) - dx;

    await drawPoint(x, y);

    let i = 1;

    while(i <= dx) {
        if(e >= 0) {
            y = y + 1;
            e = e - (2* dx);
        } 
        
            x = x + 1;
            e = e + 2 * dy;
            i = i + 1;
        
        
        await drawPoint(x, y);
    }
}