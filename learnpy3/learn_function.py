#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' learn function module '

__author__ = 'Zongchang Jie'

import os

try:
    # Python 3
    from collections.abc import Iterable
    from collections.abc import Iterator
except ImportError:
    # Python 2.7
    from collections.abc import Iterable
    from collections.abc import Iterator


# Python函数在定义的时候，默认参数li
# li的值就被计算出来了，即[]，
# 因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，
# 如果改变了li的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了。
def add_end00(li=[]):
    li.append('END')
    return li


# 定义默认参数要牢记一点：默认参数必须指向不变对象！
def add_end(li=None):
    if li is None:
        li = []
    li.append('END')
    return li


# 定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple
def calc(*numbers):
    s = 0
    for n in numbers:
        s = s + n * n
    return s


# 关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict
def person(name, age, **kw):
    if 'city' in kw:
        # 有city参数
        print(name, 'is ', age, 'years old, worked at ', kw['city'])
        pass
    if 'job' in kw:
        # 有job参数
        pass
    print('name:', name, 'age:', age, 'other:', kw)


def visitor(name, age, *, city='Beijing', job):
    print(name, age, city, job)


def visitor_one(name, age, *args, city, job):
    print(name, age, args, city, job)


def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)


def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)


def fact(n):
    if n == 1:
        return 1
    print(n, '* fact(%d)' % (n - 1))
    return n * fact(n - 1)


def learn_slice():
    li = list(range(100))
    print(li)
    # 前十个数
    print(li[:10])
    # 后十个数
    print(li[-10:])
    # 前11-20个数
    print(li[10:20])
    # 前十个数，每两个取一个
    print(li[:10:2])
    # 所有数，每五个取一个
    print(li[::5])
    print((0, 1, 2, 3, 4, 5)[:3])
    print('ABCDEFG'[:3])
    print('ABCDEFG'[::2])


def learn_iterable():
    print(isinstance('abc', Iterable))
    print(isinstance([1, 2, 3], Iterable))
    print(isinstance(123, Iterable))
    for i, val in enumerate(['A', 'B', 'C']):
        print(i, val)
    for x, y in [(1, 1), (2, 4), (3, 9)]:
        print(x, y)


# 凡是可作用于for循环的对象都是Iterable类型；
# 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
# 集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
def learn_iterator():
    print(isinstance('abc', Iterator))
    print(isinstance([], Iterator))
    print(isinstance(generator_fibonacci(3), Iterator))
    arr = (1, 2, 3, 4, 5)
    for i in arr:
        print(i)
    it = iter(arr)
    while True:
        try:
            n = next(it)
            print(n)
        except StopIteration:
            break


def learn_list_comprehensions():
    y = list(range(1, 11))
    print(y)
    li = []
    for x in range(1, 11):
        li.append(x * x)
    y = [x * x for x in range(1, 11)]
    print(y)
    # for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：
    y = [x * x for x in range(1, 11) if x % 2 == 0]
    print(y)
    y = [m + n for m in 'ABC' for n in 'XYZ']
    print(y)
    # os.listdir可以列出文件和目录
    y = [d for d in os.listdir('.')]
    print(y)
    d = {'x': 'A', 'y': 'B', 'z': 'C'}
    y = [k + '=' + v for k, v in d.items()]
    print(y)
    li = ['Hello', 'World', 'IBM', 'Apple']
    y = [s.lower() for s in li]
    print(y)


def func_fibonacci(m):
    # 斐波拉契数列（Fibonacci），除第一个和第二个数外，任意一个数都可由前两个数相加得到
    n, a, b = 0, 0, 1
    while n < m:
        print(b)
        a, b = b, a + b
        n = n + 1
    return 'done'


def generator_fibonacci(m):
    # 如果一个函数定义中包含yield关键字，那么这个函数就不再是一个普通函数，而是一个generator
    # generator和函数的执行流程不一样。函数是顺序执行，遇到return语句或者最后一行函数语句就返回。
    # 而变成generator的函数，在每次调用next()的时候执行，遇到yield语句返回，再次执行时从上次返回的yield语句处继续执行
    n, a, b = 0, 0, 1
    while n < m:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'


def learn_generator():
    # 如果列表元素可以按照某种算法推算出来，那在循环的过程中不断推算出后续的元素机制称为生成器：generator
    g = (x * x for x in range(10))
    y = next(g)
    print(y)
    for n in g:
        print(n)
    func_fibonacci(6)
    for n in generator_fibonacci(7):
        print(n)


if __name__ == '__main__':
    x = add_end00()
    print(x)
    x = add_end00()
    print(x)
    print('````````````````````````````````````````````````````````')
    x = add_end()
    print(x)
    x = add_end()
    print(x)
    print('````````````````````````````````````````````````````````')
    x = calc(1, 2)
    print('calc(1, 2) =', x)
    nums = [1, 2, 3]
    x = calc(*nums)
    print('calc([1, 2, 3]) = ', x)
    print('````````````````````````````````````````````````````````')
    person('Michael', 30)
    person('Bob', 35, city='Beijing')
    extra = {'city': 'Beijing', 'job': 'Engineer'}
    person('Jack', 24, **extra)
    print('````````````````````````````````````````````````````````')
    visitor('Jack', 24, city='Beijing', job='Engineer')
    visitor('Jack', 24, job='Engineer')
    visitor_one('Jack', 24, city='Beijing', job='Engineer')
    print('````````````````````````````````````````````````````````')
    # 参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
    f1(1, 2)
    f1(1, 2, c=3)
    f1(1, 2, 3, 'a', 'b')
    f1(1, 2, 3, 'a', 'b', x=99)
    f2(1, 2, d=99, ext=None)
    args = (1, 2, 3, 4)
    kw = {'d': 99, 'x': '#'}
    f1(*args, **kw)
    args = (1, 2, 3)
    f2(*args, **kw)
    print('````````````````````````````````````````````````````````')
    # Python标准的解释器没有针对尾递归做优化，任何递归函数都存在栈溢出的问题。
    x = fact(5)
    print(x)
    print('````````````````````````````````````````````````````````')
    learn_slice()
    print('````````````````````````````````````````````````````````')
    learn_iterable()
    print('````````````````````````````````````````````````````````')
    learn_iterator()
    print('````````````````````````````````````````````````````````')
    learn_list_comprehensions()
    print('````````````````````````````````````````````````````````')
    learn_generator()
