def func(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


for i in func(10):
    print(i, end=' ')

