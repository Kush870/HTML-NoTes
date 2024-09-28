// Setup canvas
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

canvas.width = 480;
canvas.height = 320;

// Paddle
const paddle = {
    width: 75,
    height: 10,
    x: (canvas.width - 75) / 2,
    dx: 7
};

// Ball
let ball = {
    x: canvas.width / 2,
    y: canvas.height - 30,
    radius: 10,
    dx: 2,
    dy: -2
};

// Bricks
const brick = {
    rowCount: 3,
    columnCount: 5,
    width: 75,
    height: 20,
    padding: 10,
    offsetTop: 30,
    offsetLeft: 30
};

let bricks = [];
function resetBricks() {
    bricks = [];
    for (let c = 0; c < brick.columnCount; c++) {
        bricks[c] = [];
        for (let r = 0; r < brick.rowCount; r++) {
            bricks[c][r] = { x: 0, y: 0, status: 1 }; // 1 means the brick is not broken
        }
    }
}

// Initialize bricks for the first time
resetBricks();

// Controls
let rightPressed = false;
let leftPressed = false;

// Draw paddle
function drawPaddle() {
    ctx.beginPath();
    ctx.rect(paddle.x, canvas.height - paddle.height, paddle.width, paddle.height);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

// Draw ball
function drawBall() {
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

// Draw bricks
function drawBricks() {
    for (let c = 0; c < brick.columnCount; c++) {
        for (let r = 0; r < brick.rowCount; r++) {
            if (bricks[c][r].status == 1) {
                let brickX = (c * (brick.width + brick.padding)) + brick.offsetLeft;
                let brickY = (r * (brick.height + brick.padding)) + brick.offsetTop;
                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;
                ctx.beginPath();
                ctx.rect(brickX, brickY, brick.width, brick.height);
                ctx.fillStyle = "#0095DD";
                ctx.fill();
                ctx.closePath();
            }
        }
    }
}

// Draw everything
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawBricks();
    drawBall();
    drawPaddle();
    collisionDetection();
    moveBall();
    movePaddle();
    requestAnimationFrame(draw);
}

// Move the ball
function moveBall() {
    ball.x += ball.dx;
    ball.y += ball.dy;

    // Bounce off the walls
    if (ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius) {
        ball.dx = -ball.dx;
    }
    if (ball.y + ball.dy < ball.radius) {
        ball.dy = -ball.dy;
    } else if (ball.y + ball.dy > canvas.height - ball.radius) {
        if (ball.x > paddle.x && ball.x < paddle.x + paddle.width) {
            ball.dy = -ball.dy;
        } else {
            ball.dx = 0;
            ball.dy = 0; // Stop the ball
        }
    }
}

// Move the paddle
function movePaddle() {
    if (rightPressed && paddle.x < canvas.width - paddle.width) {
        paddle.x += paddle.dx;
    } else if (leftPressed && paddle.x > 0) {
        paddle.x -= paddle.dx;
    }
}

// Collision detection
function collisionDetection() {
    for (let c = 0; c < brick.columnCount; c++) {
        for (let r = 0; r < brick.rowCount; r++) {
            let b = bricks[c][r];
            if (b.status == 1) {
                if (ball.x > b.x && ball.x < b.x + brick.width && ball.y > b.y && ball.y < b.y + brick.height) {
                    ball.dy = -ball.dy;
                    b.status = 0; // Set brick as broken
                }
            }
        }
    }
}

// Keyboard event listeners
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

function keyDownHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = true;
    } else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {
    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = false;
    } else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = false;
    }
}

// Restart game function
function restartGame() {
    // Reset ball
    ball.x = canvas.width / 2;
    ball.y = canvas.height - 30;
    ball.dx = 2;
    ball.dy = -2;

    // Reset paddle
    paddle.x = (canvas.width - paddle.width) / 2;

    // Reset bricks
    resetBricks();
}

// Start game
draw();
