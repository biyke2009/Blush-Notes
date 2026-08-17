from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Blush Notes - Tree</title>
    <style>
        body { 
            margin: 0; 
            background-color: #000; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
        }
        canvas { background-color: #000; }
    </style>
</head>
<body>
    <canvas id="treeCanvas" width="800" height="600"></canvas>
    <script>
        const canvas = document.getElementById('treeCanvas');
        const ctx = canvas.getContext('2d');

        function drawTree(length) {
            if (length < 10) return;

            // Рисуем коричневую ветку
            ctx.strokeStyle = '#5c2c16'; 
            ctx.lineWidth = Math.max(1, length / 12);
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(0, -length);
            ctx.stroke();

            // Перемещаем начало координат к концу ветки
            ctx.translate(0, -length);

            // Рисуем розовый цветок
            ctx.fillStyle = 'pink';
            ctx.beginPath();
            ctx.arc(0, 0, 3, 0, 2 * Math.PI);
            ctx.fill();

            // Левое ответвление (-20 градусов)
            ctx.save();
            ctx.rotate(-20 * Math.PI / 180);
            drawTree(4 * length / 5);
            ctx.restore();

            // Правое ответвление (+20 градусов)
            ctx.save();
            ctx.rotate(20 * Math.PI / 180);
            drawTree(4 * length / 5);
            ctx.restore();

            // Возвращаем координаты обратно
            ctx.translate(0, length);
        }

        // Устанавливаем точку старта внизу по центру
        ctx.translate(canvas.width / 2, canvas.height - 40);
        drawTree(130); // Длина основного ствола
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def read_root():
    return html_content
