import chisel3._
import chisel3.util._

class GCD extends Module {
  val io = IO(new Bundle {
    val a     = Input(UInt(16.W))
    val b     = Input(UInt(16.W))
    val loadingValues = Input(Bool())
    val outputGCD     = Output(UInt(16.W))
    val outputValid   = Output(Bool())
  })

  val x = Reg(UInt())
  val y = Reg(UInt())

  when(x > y) { x := x - y }
    .otherwise { y := y - x }

  when(io.loadingValues) {
    x := io.a
    y := io.b
  }

  io.outputGCD := x
  io.outputValid := y === 0.U
}
