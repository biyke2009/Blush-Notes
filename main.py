from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Blush Notes - Heart Tree</title>
    <style>
        body { 
            margin: 0; 
            background-color: #0d0d0d; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            overflow: hidden;
        }
        canvas { 
            box-shadow: 0 0 20px rgba(255, 192, 203, 0.2);
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <canvas id="treeCanvas" width="800" height="700"></canvas>
    <script>
        const canvas = document.getElementById('treeCanvas');
        const ctx = canvas.getContext('2d');

        let currentProgress = 0; // Прогресс анимации от 0 до 1

        function drawBranch(length, depth, maxDepth) {
            if (length < 8) return;

            // Вычисляем, насколько эта ветка уже должна вырасти
            const branchProgress = Math.min(1, Math.max(0, (currentProgress * maxDepth - depth)));
            if (branchProgress <= 0) return;

            const currentLength = length * branchProgress;

            ctx.save();

            // Рисуем ветку (ствол темнее, верхние ветки светлее)
            ctx.strokeStyle = `rgba(92, 44, 22, ${0.3 + branchProgress * 0.7})`; 
            ctx.lineWidth = Math.max(1, length / 10);
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(0, -currentLength);
            ctx.stroke();

            ctx.translate(0, -currentLength);

            // Если ветка выросла до конца и это конечная ветвь — рисуем распускающийся цветок
            if (branchProgress >= 1) {
                if (length * 0.8 < 8 || depth > 8) {
                    // Размер цветка плавно увеличивается в зависимости от общего прогресса
                    const flowerProgress = Math.min(1, (currentProgress - (depth / maxDepth)) * 3);
                    if (flowerProgress > 0) {
                        ctx.fillStyle = `rgba(255, 182, 193, ${flowerProgress * 0.85})`;
                        ctx.beginPath();
                        // Рисуем лепесток-кружочек, который плавно увеличивается в диаметре
                        ctx.arc(0, 0, 3.5 * flowerProgress, 0, 2 * Math.PI);
                        ctx.fill();
                    }
                }
            }

            // Масштабируем углы так, чтобы верхние ветви формировали очертания сердца
            // Левые ветви наклоняем чуть сильнее, правые чуть слабее в зависимости от глубины
            const leftAngle = (24 - depth * 0.5) * Math.PI / 180;
            const rightAngle = (24 - depth * 0.5) * Math.PI / 180;

            // Левое ответвление
            ctx.save();
            ctx.rotate(-leftAngle);
            drawBranch(length * 0.82, depth + 1, maxDepth);
            ctx.restore();

            // Правое ответвление
            ctx.save();
            ctx.rotate(rightAngle);
            drawBranch(length * 0.82, depth + 1, maxDepth);
            ctx.restore();

            ctx.restore();
        }

        function animate() {
            // Очищаем экран перед каждым кадром
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.save();
            // Точка старта: внизу по центру
            ctx.translate(canvas.width / 2, canvas.height - 60);

            // Запускаем рекурсивную отрисовку дерева (максимальная глубина 12 уровней)
            drawBranch(135, 0, 12);
            ctx.restore();

            // Скорость роста дерева
            if (currentProgress < 1.5) { 
                currentProgress += 0.005; 
                requestAnimationFrame(animate);
            }
        }

        // Запуск анимации при загрузке страницы
        animate();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_content
