#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import reduce
import functools


def add(x, y, f):
    return f(x) + f(y)


def learn_higher_order_func():
    x = -5
    y = 6
    f = abs
    print(add(x, y, f))


def square(x):
    return x * x


def add_xy(x, y):
    return x + y


def fn(x, y):
    return x * 10 + y


def char2num(s):
    return DIGITS[s]


DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}


def str2int(s):
    def f_xy(x, y):
        return x * 10 + y

    def char2digit(c):
        return DIGITS[c]

    return reduce(f_xy, map(char2digit, s))


def str2int_lambda(s):
    return reduce(lambda x, y: x * 10 + y, map(lambda c: DIGITS[c], s))


def learn_map_reduce():
    # map()传入的第一个参数是f，即函数对象本身。
    # 由于结果r是一个Iterator，Iterator是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list。
    r = map(square, range(1, 5))
    for n in r:
        print(n)
    print(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])))
    # reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
    li = list(range(1, 10, 2))
    print(li)
    r = reduce(add_xy, li)
    print(r)
    r = reduce(fn, map(char2num, '13579'))
    print(r)
    print(str2int('456789'))
    print(str2int_lambda('57849'))


def is_odd(n):
    return n % 2 == 1


def not_empty(s):
    return s and s.strip()


# 构造一个从3开始的奇数序列
def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


def _not_divisible(n):
    # 关键字lambda表示匿名函数，冒号前面的x表示函数参数。
    # 匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
    return lambda x: x % n > 0


def primes():
    yield 2
    it = _odd_iter()  # 初始序列
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)


def learn_filter():
    # filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
    y = list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
    print(y)
    y = list(filter(not_empty, ['A', '', 'B', None, 'C', ' ']))
    print(y)
    # 计算素数的一个方法是埃氏筛法
    for n in primes():
        if n < 100:
            print(n)
        else:
            break


def learn_sorted():
    init_li = [36, 5, -12, 9, -21]
    li = sorted(init_li)
    print(li)
    li = sorted(init_li, key=abs)
    print(li)
    init_li = ['bob', 'about', 'Zoo', 'Credit']
    li = sorted(init_li, key=str.lower)
    print(li)
    li = sorted(init_li, key=str.lower, reverse=True)
    print(li)


def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax

    return sum


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


def count_mod():
    def f(j):
        def g():
            return j * j

        # 返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。
        return g

    fs = []
    for i in range(1, 4):
        fs.append(f(i))  # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


def learn_closure():
    # 在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
    # 当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”
    f = lazy_sum(1, 3, 5, 7, 9)
    print(f())
    f1, f2, f3 = count()
    print(f1(), f2(), f3())
    f1, f2, f3 = count_mod()
    print(f1(), f2(), f3())


def log(text):
    def decorator(func):
        @functools.wraps(func)  # 把原始函数的__name__等属性复制到wrapper()函数中
        def wrapper(*args, **kw):
            print('%s %s()' % (text, func.__name__))
            return func(*args, **kw)

        return wrapper

    return decorator


@log('execute')
def now():
    print('2018/12/11')


def learn_decorator():
    now()
    print(now.__name__)


def learn_partial_function():
    # functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
    int2 = functools.partial(int, base=2)
    print(int2('1000000'))


if __name__ == '__main__':
    learn_higher_order_func()
    learn_map_reduce()
    learn_filter()
    learn_sorted()
    learn_closure()
    learn_decorator()
