import numbers

class Expression:

    def __init__(self, *operands):
        self.operands = operands
    
    def __add__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Add(self, value)
    
    def __sub__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Sub(self, value)
    
    def __mul__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Mul(self, value)
    
    def __truediv__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Div(self, value)
    
    def __pow__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Pow(self, value)
    
    def __radd__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Add(value, self)
    
    def __rsub__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Sub(value, self)
    
    def __rmul__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Mul(value, self)
    
    def __rtruediv__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Div(value, self)
    
    def __rpow__(self, value):
        if isinstance(value, numbers.Number):
            value = Number(value)
        else:
            value = Symbol(value)
        return Pow(value, self)

class Terminal(Expression):
    precedence = 0

    def __init__(self, value):
        self.value = value
        super().__init__(value)
    
    def __repr__(self):
        return repr(self.value)
    
    def __str__(self):
        return str(self.value)

class Number(Terminal):
    pass

class Symbol(Terminal):
    pass

class Operator(Expression):

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)
    
    def __str__(self):
        self.brackets = [[''] * 2] * 2
        newlist = [None] * len(self.operands)
        '''
        for x in self.operands:
            if isinstance(x, Number) or isinstance(x, Symbol):
                x.precedence = self.precedence
        '''
        newlist = self.operands
        '''
        for i in range(len(self.operands)):
            if isinstance(self.operands[i], numbers.Number):
                newlist[i] = Number(self.operands[i])
                newlist[i].precedence = self.precedence
            elif str(self.operands[i]).isalpha():
                newlist[i] = Symbol(self.operands[i])
                newlist[i].precedence = self.precedence
            else:
                newlist[i] = self.operands[i]
        '''
        for i in range(len(newlist)):
            if newlist[i].precedence > self.precedence:
                self.brackets[i] = ['(', ')']
        return f'{self.brackets[0][0]}{self.operands[0]}{self.brackets[0][1]} {self.symbol} {self.brackets[1][0]}{self.operands[1]}{self.brackets[1][1]}'

class Add(Operator):
    precedence = 6
    symbol = '+'

class Sub(Operator):
    precedence = 6
    symbol = '-'

class Mul(Operator):
    precedence = 5
    symbol = '*'

class Div(Operator):
    precedence = 5
    symbol = '/'

class Pow(Operator):
    precedence = 3
    symbol = '^'

x = Symbol('x')
y = Symbol('y')

a = (x + 1)**(y*x**3) + y**2*x*(2 / y)
b = (1/x + 1/y)**2 + (1 + 2*x)
c = 4*(x/y)**(0.5)

expra = '(x + 1) ^ (y * x ^ 3) + y ^ 2 * x * 2 / y'
exprb = '(1 / x + 1 / y) ^ 2 + 1 + 2 * x'
exprc = '4 * (x / y) ^ 0.5'

print(str(a))
print(str(b))
print(str(c))
