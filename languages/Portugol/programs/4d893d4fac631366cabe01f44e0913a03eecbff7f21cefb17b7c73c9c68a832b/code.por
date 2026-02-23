programa
{
	funcao inicio()
	{
		inteiro numero

		escreva("Quantos elementos da sequencia de Fibonacci deseja calcular? ")
		leia(numero)

		para (inteiro i = 1; i <= numero ; i++)
		{
			escreva(fibonacci(i), " ")
		}

		escreva("\n")
	}

	funcao inteiro fibonacci(inteiro posicao)
	{
		se (posicao == 1)
		{
			retorne 0
		}
		senao se (posicao == 2)
		{
			retorne 1
		}

		retorne fibonacci(posicao - 1) + fibonacci(posicao - 2)
	}
}
