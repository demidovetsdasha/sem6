export async function draw(a, b, drawPoint) {
    let x = 0;
    let y = b;
    let limit = 0;

    let delta = a*a + b*b - 2*a*a*b;

    drawPoint(x, y);

    while(y > limit) {
        if(delta > 0) {
            let d = 2*delta - 2*x - 1;

            if(d > 0)
            {
                y = y - 1;
                delta = delta - a*a*(1 - 2*y);

                await drawPoint(x, y);

                continue;
            }
        }
        
        if(delta < 0) {
            let d = 2*delta + 2*a*a*y - 1;

            if (d <= 0) {
                x = x + 1;
                delta = delta + b*b*(2*x+1);

                await drawPoint(x, y);

                continue;
            }
        }

        x = x + 1;
        y = y - 1;
        delta = delta + b*b*(2*x+1) + a*a*(1 - 2*y);

        await drawPoint(x, y);
    }
}