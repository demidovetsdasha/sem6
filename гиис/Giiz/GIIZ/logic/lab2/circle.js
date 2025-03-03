export async function draw(radius, drawPoint) {
    let x = 0;
    let y = radius;
    let limit = 0;

    let delta = 2 - 2 * radius;

    drawPoint(x, y);

    while(y > limit) {
        if(delta > 0) {
            let d = 2*delta - 2*x - 1;

            if(d > 0)
            {
                y = y - 1;
                delta = delta - 2*y  + 1;

                await drawPoint(x, y);

                continue;
            }
        }
        
        if(delta < 0) {
            let d = 2*delta + 2*y - 1;

            if (d <= 0) {
                x = x + 1;
                delta = delta + 2*x + 1;

                await drawPoint(x, y);

                continue;
            }
        }

        x = x + 1;
        y = y - 1;
        delta = delta + 2*x - 2*y + 2;

        await drawPoint(x, y);
    }
}