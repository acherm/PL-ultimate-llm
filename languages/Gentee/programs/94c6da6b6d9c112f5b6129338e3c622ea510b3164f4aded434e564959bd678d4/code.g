run {
    int count = 20
    int a = 0
    int b = 1
    for i in 0..count {
        Println(str(a))
        int temp = a + b
        a = b
        b = temp
    }
}
