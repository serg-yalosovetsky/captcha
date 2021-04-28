from re import A
import uuid

uu = uuid.uuid4()
uu

a = []
b = a
a.append('asdf')
b

def f():
    x=1

def one():
    x = ['one', 'two']
    def inner():
        print(x)
        print(id(x))
    return inner

o = one()
o()
a = o.__closure__[0].cell_contents
id(a)
a.append('asdf')
one()()
