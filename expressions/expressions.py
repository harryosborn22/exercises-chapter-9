import numbers

def postvisitor(expr, fn, **kwargs):
    tree = expr
    calcstack = []
    newstack =[]
    while expr.operands:
        calcstack.append(expr.symbol[1])
        expr = expr.operands
        print("hi")
        expr = []
    

def ifnumber(value):
    if isinstance(value, numbers.Number):
        return Number(value)
    else:
        return value

class Expression:
    def __init__(self, *operands):
        self.operands = operands

    def __add__(self, value):
        return Add(self, ifnumber(value))

    def __sub__(self, value):
        return Sub(self, ifnumber(value))

    def __mul__(self, value):
        return Mul(self, ifnumber(value))

    def __truediv__(self, value):
        return Div(self, ifnumber(value))

    def __pow__(self, value):
        return Pow(self, ifnumber(value))

    def __radd__(self, value):
        return Add(ifnumber(value), self)

    def __rsub__(self, value):
        return Sub(ifnumber(value), self)

    def __rmul__(self, value):
        return Mul(ifnumber(value), self)

    def __rtruediv__(self, value):
        return Div(ifnumber(value), self)

    def __rpow__(self, value):
        return Pow(ifnumber(value), self)

class Operator(Expression):
    
    def __repr__(self):
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        stringbuild = ''
        for i in range(len(self.operands)):
            if self.operands[i].precedence > self.precedence:
                stringbuild += (f'{self.symbol * i}'
                               f'({str(self.operands[i])})')
            else:
                stringbuild += (f'{self.symbol * i}'
                                f'{str(self.operands[i])}')
        return stringbuild

class Add(Operator):
    precedence = 3
    symbol = ' + '

class Sub(Operator):
    precedence = 3
    symbol = ' - '

class Mul(Operator):
    precedence = 2
    symbol = ' * '

class Div(Operator):
    precedence = 2
    symbol = ' / '

class Pow(Operator):
    precedence = 1
    symbol = ' ^ '

class Terminal(Expression):
    precedence = 0

    def __init__(self, value, *operands):
        self.value = value
        super().__init__(self.value)
    
    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

class Number(Terminal):
    pass

class Symbol(Terminal):
    pass

from functools import singledispatch
import expressions


@singledispatch
def evaluate(expr, *o, **kwargs):
    """Evaluate an expression node.

    Parameters
    ----------
    expr: Expression
        The expression node to be evaluated.
    *o: numbers.Number
        The results of evaluating the operands of expr.
    **kwargs:
        Any keyword arguments required to evaluate specific types of
        expression.
    symbol_map: dict
        A dictionary mapping Symbol names to numerical values, for
        example:

        {'x': 1}
    """
    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@evaluate.register(expressions.Number)
def _(expr, *o, **kwargs):
    return expr.value


@evaluate.register(expressions.Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return symbol_map[expr.value]


@evaluate.register(expressions.Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@evaluate.register(expressions.Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@evaluate.register(expressions.Mul)
def _(expr, *o, **kwargs):
    return o[0] * o[1]


@evaluate.register(expressions.Div)
def _(expr, *o, **kwargs):
    return o[0] / o[1]


@evaluate.register(expressions.Pow)
def _(expr, *o, **kwargs):
    return o[0] ** o[1]


x = Symbol('x')

y = Symbol('y')

expr = 3*x + 2**(y/5) - 1

postvisitor(expr, evaluate, symbol_map={'x': 1.5, 'y': 10})