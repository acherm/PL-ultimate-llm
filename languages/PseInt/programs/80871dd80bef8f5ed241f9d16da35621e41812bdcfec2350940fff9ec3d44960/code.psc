Algoritmo Fibonacci
    Definir n, i, a, b, temp Como Entero
    Escribir "Ingrese la cantidad de terminos de Fibonacci:"
    Leer n
    a <- 0
    b <- 1
    Escribir "Serie de Fibonacci:"
    Para i <- 1 Hasta n Hacer
        Escribir a
        temp <- a + b
        a <- b
        b <- temp
    FinPara
FinAlgoritmo
