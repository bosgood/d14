export var seed = 0
export function sliderSeed(v) {
  seed = v
}

export var colorSpeed = 0.1
export function sliderColorSpeed(v) {
  colorSpeed = v
}

export var fadeSpeed = 1
export function sliderFadespeed(v) {
  fadeSpeed = v
}

export var rotationSpeed = 25
export function sliderRotationSpeed(v) {
  rotationSpeed = v * 100
}

// Pink RGB = 253, 0, 152
// Orange RGB = 253, 76, 0
var rgbGradient = [
  0.00, 0.9921, 0,      0.5960,
  0.25, 0,      0,      0,
  0.50, 0,      0,      0,
  0.75, 0,      0,      0,
  1.00, 0.9921, 0.2980, 0,
]

acc = 0
rotationDeg = 0


export function beforeRender(delta) {
  setPalette(rgbGradient)
  t1 = wave(time(colorSpeed))
  t2 = wave(time(fadeSpeed))
  
  // Timed change of value
  acc += delta
  if (acc < rotationSpeed) {
    return
  }
  acc = 0  

  // Rotate 2D canvas
  resetTransform()
  rotationDeg = (rotationDeg + 1) % 360
  rotate(rotationDeg * PI/180)
}

export function render2D(index, x, y) {
  noiseVal1 = perlin(x, y, t1, seed)
  mapped1 = mapVal(noiseVal1, -0.5, 0.5, 0, 1)
  
  noiseVal2 = perlin(y, x, t2, seed)
  mapped2 = mapVal(noiseVal2, -0.5, 0.5, 0, 1)
  paint(mapped1, mapped2)
}

function mapVal(value, istart, istop, ostart, ostop) {
  return ostart + (ostop - ostart) * ((value - istart) / (istop - istart));
}
