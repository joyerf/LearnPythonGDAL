#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math


def basic_print():
    print('I\'m ok.')
    # 转义
    print('\\\t\\')
    print(r'\\\t\\')
    # 多行输出
    print('''line1
line2
lin3''')


def string_handle():
    # 字符，字符串
    print('包含中文的string')
    print(ord('A'))
    print(chr(66))
    print(ord('中'))
    print(chr(25991))
    print('\u4e2d\u6587')
    print()
    # 编解码
    x = 'ABC'.encode('ascii')
    print(x)
    x = '中文'.encode('utf-8')
    print(x)
    x = b'ABC'.decode('ascii')
    print(x)
    # errors='ignore'忽略错误的字节
    x = b'\xe4\xb8\xad\xe6\x96\x87'.decode('utf-8', errors='ignore')
    print(x)
    x = len(b'ABC')
    print(x)
    # 格式化
    x = 'Hi, %s, you have $%d.' % ('Michael', 1000000)
    print(x)
    print('%2d-%02d' % (3, 1))
    print('%.2f' % 3.1415926)
    print('growth rate: %d %%' % 7)
    print('Age: %s. Gender: %s' % (25, True))
    print('Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125))
    # 当我们调用a.replace('a', 'A')时，实际上调用方法replace是作用在字符串对象'abc'上的，
    # 而这个方法虽然名字叫replace，但却没有改变字符串'abc'的内容。
    # 相反，replace方法创建了一个新字符串'Abc'并返回，如果我们用变量b指向该新字符串，就容易理解了，
    # 变量a仍指向原有的字符串'abc'，但变量b却指向新字符串'Abc'了
    a = 'abca'
    b = a.replace('a', 'A')
    print('a=', a, 'b=', b)


def learn_list():
    classmates = ['Michael', 'Bob', 'Tracy']
    print(classmates)
    print(len(classmates))
    print(classmates[1])
    print(classmates[0])
    # 倒数第一个
    print(classmates[-1])
    # 倒数第二个
    print(classmates[-2])
    classmates.append('Adam')
    print(classmates)
    classmates.insert(1, 'Jack')
    print(classmates)
    print(classmates.pop())  # 删除list末尾的元素
    print(classmates)
    print(classmates.pop(1))  # 删除指定位置的元素
    print(classmates)

    li = ['Apple', 123, True]
    print(li)
    s = ['Orange', li, 'java']
    print(s[1][0])


def learn_tuple():
    # 能用tuple代替list就尽量用tuple
    classmates = ('Michael', 'Bob', 'Tracy')  # tuple一旦初始化就不能修改
    print(classmates)
    t = (1,)  # 只有1个元素的tuple定义时必须加一个逗号,
    print(t)
    t = ('a', 'b', ['A', 'B'])
    print(t)
    t[2][0] = 'X'
    t[2][1] = 'Y'
    print(t)


def learn_for():
    names = ['Michael', 'Bob', 'Tracy']
    for name in names:
        print(name)
    sum_ = 0
    for x in [1, 2, 3, 4, 5]:
        sum_ += x
    print(sum_)
    li = list(range(5))
    print(li)
    for x in range(101):
        sum_ = sum_ + x
    print(sum_)


def learn_dictionary():
    # dict的key必须是不可变对象。
    d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
    print(d['Michael'])
    d['Adam'] = 67
    print('Thomas' in d)
    x = d.get('Thomas')
    print(x)
    d.pop('Bob')
    print(d)
    # set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
    s = {1, 2, 3}
    print(s)
    s = set([1, 1, 2, 2, 3, 3])
    print(s)
    s.add(4)
    print(s)
    s.remove(2)
    print('s=', s)
    # set可以看成数学意义上的无序和无重复元素的集合，因此，两个set可以做数学意义上的交集、并集等操作
    s2 = {1, 2, 3, 6, 7}
    print('s2=', s2)
    print(s & s2)
    print(s | s2)


def move(x, y, step, angle=0):
    nx = x + step * math.cos(angle)
    ny = y - step * math.sin(angle)
    # 在语法上，返回一个tuple可以省略括号
    return nx, ny


def my_func_test(m):
    if not isinstance(m, (int, float)):
        raise TypeError('bad operand type')
    if m < 0:
        x, y = move(100, 100, 60, math.pi / 6)
        print('move', x, y)
        pass
    else:
        x, y = move(200, 200, 60, math.pi / 6)
        print('move', x, y)
        return m


if __name__ == '__main__':
    basic_print()
    string_handle()
    learn_list()
    learn_tuple()
    learn_for()
    learn_dictionary()
    my_func_test(-1)
    my_func_test(2)
