float angle = 0;
float radius = 0;

void setup() {
  size(400, 400);
  background(0);
  stroke(255);
  noFill();
}

void draw() {
  translate(width/2, height/2);
  
  float x = cos(angle) * radius;
  float y = sin(angle) * radius;
  
  point(x, y);
  
  angle += 0.1;
  radius += 0.1;
  
  if (radius > width/2) {
    background(0);
    radius = 0;
  }
}