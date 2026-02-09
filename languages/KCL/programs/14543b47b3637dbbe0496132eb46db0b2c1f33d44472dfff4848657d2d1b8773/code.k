import regex

schema Sample:
    foo: str
    bar: int
    fooList: [str]
    check:
        bar > 0
        bar < 100
        len(fooList) > 0
        len(fooList) < 100
        regex.match(foo, "^The.*Foo$")
        isunique(fooList)
        bar in range(100)
        bar in [2, 4, 6, 8]
        multiplyof(bar, 2)

goodSample = Sample {
    foo = "The Foo"
    bar = 2
    fooList = ["foo0", "foo1"]
}

badSample = Sample {
    foo = "The Foo"
    bar = 123
    fooList = ["foo0", "foo1"]
}
