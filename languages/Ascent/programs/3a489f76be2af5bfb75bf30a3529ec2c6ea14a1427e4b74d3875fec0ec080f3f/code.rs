use ascent::ascent;

ascent! {
   relation edge(i32, i32);
   relation path(i32, i32);

   path(x, y) <-- edge(x, y);
   path(x, z) <-- edge(x, y), path(y, z);
}

fn main() {
   let mut prog = AscentProgram::default();
   prog.edge = vec![(1, 2), (2, 3), (3, 4)];
   prog.run();
   println!("path: {:?}", prog.path);
}
