const canvas = document.getElementById("game");
const background = "black"
const FPS = 60

game.width = 1920
game.height = 1080
const ctx = game.getContext("2d")
const lighting = {x: 0, y: 1, z: 0}

ctx.fillStyle = background
ctx.fillRect(0, 0, game.width, game.height)

function point(x, y, intensity) {
    let size = 15
    let brightness = Math.max(0, intensity) * 90; // 0-100%
    ctx.fillStyle = `hsl(120, 100%, ${brightness/2}%)`; // 120 = green hue
    ctx.fillRect(x - size/2, y - size/2, size, size)
}

function screen(p, intensity) {
    // We want x = -1 to map to 0 and x = 1 to map to game.width
    // Thus, we want to know our mapping function from [-1, 1] to [0, game.width]
    // we know (-1, 0) and (1, game.width) are two points on the line. Thus, m = (W - 0) / 1 - (-1) = W / 2
    // Now, using y - y1 = m(x - x1), we have that y - 0 = (W / 2)(x - (-1)) ====> y = (W / 2)(x + 1)

    // Height case: [-1, 1] map to [height, 0], analogous case but we end up with a factor of 1 - y instead because y grows downwards in html canvas
    const screenX = (game.width / 2) * (p.x + 1)
    const screenY = (game.height / 2) * (1 - p.y)
    point(screenX, screenY, intensity)
}

function project({x, y, z}) {
    // Simple orthographic projection
    return {x: x / z , y: y / z}
}

function rotateY({x, y, z}, alpha) {
    // Rotate around the Y axis
    const cosa = Math.cos(alpha)
    const sina = Math.sin(alpha)
    return {
        x: x * cosa - z * sina,
        y: y,
        z: x * sina + z * cosa
    }
}

function rotateX({x, y, z}, alpha) {
    const cosa = Math.cos(alpha)
    const sina = Math.sin(alpha)
    return {
        x: x,
        y: y * cosa - z * sina,
        z: y * sina + z * cosa
    }
}

let vertices = []
const R = 1
const r = 0.5
const steps = 60;

for (let alpha = 0; alpha < 2 * Math.PI; alpha += 2 * Math.PI / steps) {
    for (let phi = 0; phi < 2 * Math.PI; phi += 2 * Math.PI / steps) {
        const x = (R + r * Math.cos(phi)) * Math.cos(alpha)
        const y = (R + r * Math.cos(phi)) * Math.sin(alpha)
        const z = r*Math.sin(phi)
        const normal = {x:Math.cos(alpha) * Math.cos(phi), y:Math.sin(alpha) * Math.cos(phi), z:Math.sin(phi)}
        vertices.push({x, y, z, normal})
    }
}

const dt = 1 / FPS
let dz = 0
let angle = 0

function frame() {
    ctx.fillStyle = background
    ctx.fillRect(0, 0, game.width, game.height)
    angle += Math.PI * dt
    let buffer = []

    for (const v of vertices) {
        // First rotate, then project then screen
        let rotated = rotateY(v, angle)
        let rotatedNormal = rotateY(v.normal, angle)

        rotated = rotateX(rotated, angle)
        rotatedNormal = rotateX(rotatedNormal, angle)

        const intensity = 
            rotatedNormal.x * lighting.x +
            rotatedNormal.y * lighting.y +
            rotatedNormal.z * lighting.z
        const moved = {x: rotated.x, y: rotated.y + 1, z: rotated.z + 15}
        const projected = project(moved)
        buffer.push({p: projected, z: moved.z, intensity:intensity})
    }

    buffer.sort((a, b) => b.z - a.z)

    for (const v of buffer) {
        screen(v.p, v.intensity)
    }
    setTimeout(frame, 1000 / FPS)
}

setTimeout(frame, 1000 / FPS)

// Overall, the logic was first: we have to translate the mapping. 
// Secondly, we performed the frame function, because we run at 60 fps the function was called 60 times per second. and between calls, a time of dt = 1 / FPS has passed.
// In each frame, we clear the canvas, then for each vertex we rotate it, move it away from the camera, project it to 2D and finally map it to screen coordinates and draw it.
// It is fundamental the order is rotate -> move -> project -> screen, because each operation depends on the previous one
