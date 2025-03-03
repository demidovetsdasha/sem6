export async function draw(p, r, drawPoint) {
    // Матрица Эрмита, определяющая коэффициенты для интерполяции
    const ermitMatrics = [
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ];

    console.log(r); 

    // Вектор значений (точки + производные)
    const ermitVector = [
        p[0], // Координаты первой точки
        p[1], 
        r[0], // Производная в первой точке
        r[1], 
    ];

    for(let i = 0; i <= 1; i += 0.1) {
        let t = [[i*i*i, i*i, i, 1]];

        // Умножаем матрицу Эрмита на вектор значений (точек и производных)
        let coef = multiplyMatrices(ermitMatrics, ermitVector);

        // Получаем координаты текущей точки на кривой Эрмита
        let point = multiplyMatrices(t, coef);

        // Отрисовываем точку (асинхронно)
        await drawPoint(point[0][0], point[0][1]);
    }
}

// Функция для умножения матриц
function multiplyMatrices(mat1, mat2) {
    // Проверяем возможность умножения (число столбцов первой матрицы должно совпадать с числом строк второй)
    if (mat1[0].length !== mat2.length) {
        throw new Error("Невозможно умножить матрицы: количество столбцов первой матрицы не совпадает с количеством строк второй матрицы.");
    }

    const rows1 = mat1.length; 
    const cols2 = mat2[0].length; 
    const result = new Array(rows1);

    for (let i = 0; i < rows1; i++) {
        result[i] = new Array(cols2).fill(0);
    }

    // Само умножение 
    for (let i = 0; i < rows1; i++) {
        for (let j = 0; j < cols2; j++) {
            for (let k = 0; k < mat1[0].length; k++) {
                result[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }

    return result;
}
