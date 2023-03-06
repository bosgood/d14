// Calm pastel colors
rgbGradient = [
  0.00, 34,   139,  230,
  0.25, 121,  80,   242,
  0.50, 230,  73,   127,
  0.75, 253,  126,  19,
  1.00, 65,   192,  87,
]
brightness = 0.003

export var speed = 25
export function sliderSpeed(v) {
  speed = v * 100
}

export var scrollDistance = 0.01
export function sliderScrollSpeed(v) {
  scrollDistance = v * 0.025
}

export var noiseDistance = 0.01
export function sliderNoiseDistance(v) {
  noiseDistance = v * 0.015
}

export var displayThreshold = 0.2
export function sliderDisplayThreshold(v) {
  displayThreshold = v
}

export var seed = 1231234128
export function sliderSeed(v) {
  seed = v * 1231234128
}

acc = 0
scrollPos = 0
noisePos = 0

export function beforeRender(delta) {
  setPalette(rgbGradient)
  t1 = time(.1)
  
  // Timed change of value
  acc += delta
  if (acc < speed) {
    return
  }
  acc = 0
  scrollPos = (scrollPos + scrollDistance) % 1
  noisePos = noisePos + noiseDistance
  
  resetTransform()
  rotate(45 * PI/180)
}

export function render(index) {
  render2D(index, index / pixelCount, 0)
}

export function render2D(index, x, y) {
  noise = perlin(x, y, noisePos, seed)
  if (noise >= (-1 * displayThreshold) && noise <= displayThreshold) {
    paint(x + scrollPos, brightness)  
  }
}
  