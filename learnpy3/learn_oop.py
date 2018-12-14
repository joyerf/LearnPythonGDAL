#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import types
from types import MethodType
from enum import Enum, unique


class Student(object):
    # 用tuple定义允许绑定的属性名称
    __slots__ = ('__name', '__score', 'grade', 'print_grade')

    def __init__(self, name='NA', score=0):
        # 变量名如果以__开头，就变成了一个私有变量（private）
        self.__name = name
        self.__score = score

    def get_name(self):
        return self.__name

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        elif value < 0 or value > 100:
            raise ValueError('score must between 0~100!')
        else:
            self.__score = value

    def print_score(self):
        print('%s %s' % (self.__name, self.__score))

    def __len__(self):
        return 100

    def __str__(self):
        return 'Student object (name:%s)' % self.__name

    __repr__ = __str__


class FStudent(Student):
    # 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
    country = 'FRENCH'

    def __init__(self, name, score):
        super().__init__(name, score)
        self.country = 'USA'

    def print_score(self):
        print(self.get_name(), ' come from', self.country, self.score)

    def __getattr__(self, attr):
        if 'age' == attr:
            return lambda: 25
        elif 'gender' == attr:
            return 'female'
        else:
            raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)

    # 定义一个__call__()方法，就可以直接对实例进行调用
    def __call__(self, *args, **kwargs):
        print('My Name is %s.' % self.get_name())


class Fib(object):
    def __init__(self):
        self.__a, self.__b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.__a, self.__b = self.__b, self.__a + self.__b
        return self.__a

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        elif isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            li = []
            for x in range(stop):
                if x >= start:
                    li.append(a)
                a, b = b, a + b
            return li


class Chain(object):

    def __init__(self, path=''):
        self.__path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self.__path, path))

    def __str__(self):
        return self.__path

    __repr__ = __str__


def learn_attr():
    print(type(123) == int)
    print(type('123' == str))
    print(type(abs) == types.BuiltinFunctionType)
    print(isinstance(abs, types.BuiltinFunctionType))
    print(type(lambda x: x + 1) == types.LambdaType)
    print(type((x for x in range(10))) == types.GeneratorType)
    print(isinstance([1, 2, 3], (list, tuple)))
    # 获得一个对象的所有属性和方法
    print(dir('ABC'))
    print(len(std))
    # hasattr 有属性'x'吗？
    print(hasattr(std, '__name'))
    f_std = FStudent('Jack', 99)
    print(hasattr(f_std, 'country'))
    f_std.print_score()
    setattr(f_std, 'country', 'BU')
    f_std.score = 88
    f_std.print_score()
    # 传入一个default参数，如果属性不存在，就返回默认值
    print(getattr(f_std, 'country', 'ENG'))
    # 获取对象的方法属性'print_score'并赋值到变量fn
    fn = getattr(f_std, 'print_score')
    fn()
    # 相同名称的实例属性将屏蔽掉类属性，但是当你删除实例属性后，再使用相同的名称，访问到的将是类属性
    print(FStudent.country)
    print(f_std.country)
    del f_std.country
    print(f_std.country)


def print_grade(self):
    print(self.grade)


def learn_slots():
    s = Student('Michael', 80)
    s.grade = 'A'
    # 给实例绑定一个方法
    s.print_grade = MethodType(print_grade, s)
    s.print_grade()
    Student.print_grade = print_grade
    # 给class绑定方法后，所有实例均可调用
    s2 = Student('John', 88)
    s2.grade = 'A+'
    s2.print_grade()


def learn_special_method():
    for n in Fib():
        print(n)
        if n > 100:
            break
    print(Fib()[1:6])
    print(6, Fib()[5])
    s = FStudent('Joyce', 99)
    print(s)
    s.score = 100
    print(s.age())
    print(s.gender)
    print(Chain().starus.user.timeline.list)
    s()

    print(callable(s))
    print(callable(Student()))
    print(callable(None))


Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))


@unique  # @unique装饰器可以帮助我们检查保证没有重复值。
class Weekday(Enum):
    Sun = 0  # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6


def learn_enum():
    for name, member in Month.__members__.items():
        print(name, '=>', member, ',', member.value)
    for name, member in Weekday.__members__.items():
        print(name, '=>', member)
    day1 = Weekday.Mon
    print(day1)
    print(Weekday['Tue'])
    print(Weekday(1))


# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    # 接收到的参数依次是：
    # 1.当前准备创建的类的对象；
    # 2.类的名字；
    # 3.类继承的父类集合；
    # 4.类的方法集合。
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)


# 当我们传入关键字参数metaclass时，魔术就生效了，它指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建，
# 在此，我们可以修改类的定义，比如，加上新的方法，然后，返回修改后的定义。
class MyList(list, metaclass=ListMetaclass):
    pass


def learn_metaclass():
    print(type(Student))
    s = Student('Bob', 88)
    print(type(s))

    # type()函数既可以返回一个对象的类型，又可以创建出新的类型
    def f_new_class(self, name='world'):  # 先定义函数
        print('Hello, %s.' % name)

    # 要创建一个class对象，type()函数依次传入3个参数：
    # 1.class的名称；
    # 2.继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
    # 3.class的方法名称与函数绑定，这里我们把函数f_new_class绑定到方法名hello上。
    Hello = type('Hello', (object,), dict(hello=f_new_class))  # 创建Hello class
    h = Hello()
    h.hello()
    print(type(h))
    # metaclass是Python中非常具有魔术性的对象，它可以改变类创建时的行为。这种强大的功能使用起来务必小心。
    li = MyList()
    li.add(1)
    print(li)


if __name__ == '__main__':
    std = Student('Bob', 90)
    std.print_score()
    learn_attr()
    learn_slots()
    learn_special_method()
    learn_enum()
    learn_metaclass()
    pass
