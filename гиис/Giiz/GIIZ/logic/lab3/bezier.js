export async function draw(p, drawPoint) {
    const ermitMatrics = [
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0]
    ];

    const ermitVector = [
        p[0],
        p[1],
        p[2],
        p[3]
    ];


    for(let i = 0; i <= 1; i+=0.1) {
        let t = [[i*i*i, i*i, i, 1]];

        let coef = multiplyMatrices(ermitMatrics, ermitVector);

        let point = multiplyMatrices(t, coef);

        await drawPoint(point[0][0],point[0][1]);
    }
}

function multiplyMatrices(mat1, mat2) {

    if (mat1[0].length !== mat2.length) {
        throw new Error("Невозможно умножить матрицы: количество столбцов первой матрицы не совпадает с количеством строк второй матрицы.");
    }

    const rows1 = mat1.length;
    const cols2 = mat2[0].length;
    const result = new Array(rows1);
    for (let i = 0; i < rows1; i++) {
        result[i] = new Array(cols2).fill(0);
    }

    for (let i = 0; i < rows1; i++) {
        for (let j = 0; j < cols2; j++) {
            for (let k = 0; k < mat1[0].length; k++) {
                result[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }

    return result;
}