export async function draw(point1, point2, drawPoint) {
    const length = Math.max(
      Math.abs(point2.x - point1.x),
      Math.abs(point2.y - point1.y)
    );

    await drawPoint(point1.x, point1.y);
  
    let dx = (point2.x - point1.x) / length;
    let dy = (point2.y - point1.y) / length;
  
    let x = point1.x + 0.5 * Math.sign(dx);
    let y = point1.y + 0.5 * Math.sign(dy);
  
    await drawPoint(x, y);
  
    for (let i = 0; i < length; i++) {
      x = x + dx;
      y = y + dy;

      if(x>=point2.x && y >= point2.y) {
        await drawPoint(point2.x, point2.y);
        break;
      }
  
      await drawPoint(x, y);
    }
  }