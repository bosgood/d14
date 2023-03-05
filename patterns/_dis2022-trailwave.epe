var sparkHueO = .05;
var sparkHueP = .9;
export var numTrails = floor(pixelCount / 25);
var trails = array(numTrails);
var trailLen = 10;
var timing = 30;

// pre-allocate trails spaced evenly along sequence
for (var i = 0; i < trails.length; i++) {
  trails[i] = i * numTrails;
}


export var acc = 0;

export function beforeRender(delta) {
  t1 = time(0.5);
  t2 = time(0.5);
  t3 = time(0.5);
  w1 = clamp(wave(t1), 0.35, 0.75);
  w2 = clamp(wave(t2), 0.5, 1);
  w3 = clamp(wave(t3), 0.75, 1);
  
  acc += (delta * w1);
  if (acc < timing) {
    return;
  }
  acc = 0;
  
  // move every trail forward one pixel
  for (var i = 0; i < trails.length; i++) {
    var next = trails[i] + 1;
    if (next == pixelCount) {
      next = 0;
    }
    trails[i] = next;
  }
}

export function render(index) {
  var hue = sparkHueO;
  var pos = 0;
  for (var i = 0; i < trails.length; i++) {
    var diff = abs(trails[i] - index);
    if (diff <= trailLen) {
      pos = (1 - diff / trailLen);
      if (i % 2 > 0) {
        hue = sparkHueP;
      }
    }
  }
  
  hsv(hue, 1, pos);
}
