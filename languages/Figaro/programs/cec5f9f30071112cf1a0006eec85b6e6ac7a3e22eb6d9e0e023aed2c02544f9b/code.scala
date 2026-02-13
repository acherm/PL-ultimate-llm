import com.cra.figaro.language._
import com.cra.figaro.library.atomic.continuous.Beta
import com.cra.figaro.library.atomic.discrete.Binomial
import com.cra.figaro.algorithm.factored.VariableElimination

object CoinExample {
  def main(args: Array[String]): Unit = {
    val fairness = Beta(2, 2)
    val numberOfFlips = 10
    val numberOfHeads = Binomial(numberOfFlips, fairness)

    numberOfHeads.observe(7)

    val algorithm = VariableElimination(fairness)
    algorithm.start()

    println("Probability fairness > 0.5: " + algorithm.probability(fairness, (f: Double) => f > 0.5))

    algorithm.kill()
  }
}
