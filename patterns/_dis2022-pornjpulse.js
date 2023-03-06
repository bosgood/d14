
//  dis - pornjpulse
//  dis 2022

r =252 /255;
g = 23 / 255;
b = 218/255;

pink = [r,g,b];

export function beforeRender(delta) {
  t1 = triangle(time(.1))  // Mirror time (bounce)
}

export function render(index) {
  pct = index / pixelCount
  edge = clamp(triangle(pct) + t1 * 4 - 2, 0, 1)  // Mirror space
  
  h = edge * edge - .2  // Expand violets
  
  v = triangle(edge)    // Doubles the frequency

  //hsv(h, 1, v);
  rgb(pink[0], pink[1] , pink[2] * v);
}


