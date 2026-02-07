import spinal.core._

class Counter extends Component {
  val io = new Bundle {
    val enable = in Bool()
    val clear = in Bool()
    val count = out UInt(8 bits)
  }

  val counterReg = Reg(UInt(8 bits)) init(0)

  when(io.clear) {
    counterReg := 0
  } elsewhen(io.enable) {
    counterReg := counterReg + 1
  }

  io.count := counterReg
}

object CounterVerilog extends App {
  SpinalVerilog(new Counter)
}
