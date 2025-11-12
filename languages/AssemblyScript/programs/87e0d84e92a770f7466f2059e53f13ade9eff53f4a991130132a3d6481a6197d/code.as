class Point {
  constructor(public x: f64 = 0.0, public y: f64 = 0.0) {}

  get magnitude(): f64 {
    return Math.hypot(this.x, this.y);
  }
}

let p = new Point(3, 4);
console.log(p.magnitude); // 5