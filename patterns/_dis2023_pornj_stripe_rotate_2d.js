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
scanSpeed = 50
scanIncrement = 0.01
scanModifier = 0

rotateIncrement = 0.1
export var rotationDeg = 0

export function beforeRender(delta) {
  setPalette(rgbGradient)
  t1 = wave(time(0.1))
  t2 = wave(time(1.0))
  
  // Timed change of value
  acc += delta
  if (acc < scanSpeed) {
    return
  }
  acc = 0  

  // Scan across coordinate system to show movement
  scanModifier = (scanModifier + scanIncrement) % 1

  // Rotate 2D canvas between 2 extremes
  resetTransform()
  rotationDeg = (rotationDeg + rotateIncrement) % 360
  // Change direction of rotation at either extreme
  if (rotationDeg < 0 || rotationDeg > 100) {
    rotateIncrement = rotateIncrement * -1
  }
  rotate(rotationDeg * PI/180)
}

export function render2D(index, x, y) {
  // Scan horizontally across x axis
  paint(x + scanModifier, y)
}
