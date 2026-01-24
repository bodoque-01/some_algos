const canvas = document.getElementById("game");
console.log(game)


const background = "black"
const foreground = "green"
const FPS = 60

game.width = 1920
game.height = 1080
const ctx = game.getContext("2d")

ctx.fillStyle = background
ctx.fillRect(0, 0, game.width, game.height)

function point(x, y) {
    let size = 15
    ctx.fillStyle = foreground
    ctx.fillRect(x - size/2, y - size/2, size, size)
}

function screen(p) {
    // We want x = -1 to map to 0 and x = 1 to map to game.width
    // Thus, we want to know our mapping function from [-1, 1] to [0, game.width]
    // we know (-1, 0) and (1, game.width) are two points on the line. Thus, m = (W - 0) / 1 - (-1) = W / 2
    // Now, using y - y1 = m(x - x1), we have that y - 0 = (W / 2)(x - (-1)) ====> y = (W / 2)(x + 1)

    // Height case: [-1, 1] map to [height, 0], analogous case but we end up with a factor of 1 - y instead because y grows downwards in html canvas
    
    const screenX = (game.width / 2) * (p.x + 1)
    const screenY = (game.height / 2) * (1 - p.y)
    point(screenX, screenY)
}


function project({x, y, z}) {
    // Simple orthographic projection
    return {x: x / z , y: y / z}
}


function rotate({x, y, z}, alpha) {
    // Rotate around the Y axis
    const cosa = Math.cos(alpha)
    const sina = Math.sin(alpha)
    return {
        x: x * cosa - z * sina,
        y: y,
        z: x * sina + z * cosa
    }
}

let vertices = []

const R = 2
const r = 1

const steps = 40;

for (let alpha = 0; alpha < 2 * Math.PI; alpha += 2 * Math.PI / steps) {
    for (let phi = 0; phi < 2 * Math.PI; phi += 2 * Math.PI / steps) {
        const x = (R + r * Math.cos(phi)) * Math.cos(alpha)
        const y = (R + r * Math.cos(phi)) * Math.sin(alpha)
        const z = r*Math.sin(phi)
        vertices.push({x, y, z})
    }
}


const dt = 1 / FPS
let dz = 0
let angle = 0

function frame() {
    ctx.fillStyle = background
    ctx.fillRect(0, 0, game.width, game.height)
    angle += Math.PI * dt
    for (const v of vertices) {
        // First rotate, then project then screen
        const rotated = rotate(v, angle)
        const moved = {x: rotated.x, y: rotated.y + 1, z: rotated.z + 5}
        const projected = project(moved)
        screen(projected)
    }
    setTimeout(frame, 1000 / FPS)
}

setTimeout(frame, 1000 / FPS)

// Overall, the logic was first: we have to translate the mapping. 
// Secondly, we performed the frame function, because we run at 60 fps the function was called 60 times per second. and between calls, a time of dt = 1 / FPS has passed.
// In each frame, we clear the canvas, then for each vertex we rotate it, move it away from the camera, project it to 2D and finally map it to screen coordinates and draw it.
// It is fundamental the order is rotate -> move -> project -> screen, because each operation depends on the previous one
