import numbers
from functools import singledispatch

def number_check(value):
    if isinstance(value, numbers.Number):
            return Number(value)
    else:
        return value

def evaluatethis(self, values):
    self = str(self)
    differences = {'^' : '**'}
    for variable, value in values.items():
        self = self.replace(variable, str(value))
    for first, second in differences.items():
        self = self.replace(first, second)
    return Number(eval(self))


def postvisitor(expr, fn, **kwargs):
    '''Visit an Expression in postorder applying a function to every node.

    Parameters
    ----------
    expr: Expression
        The expression to be visited.
    fn: function(node, *o, **kwargs)
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the results of
        visiting its operands as any further positional arguments. Any
        additional information that the visitor requires can be passed in
        as keyword arguments.
    **kwargs:
        Any additional keyword arguments to be passed to fn.
    '''
    '''
    if isinstance(expr, numbers.Number):
        return Number(expr)
    elif isinstance(expr, str):
        return Symbol(expr)
    '''
    return fn(expr,
              *(postvisitor(c, fn, **kwargs) for c in expr.operands),
              **kwargs)

class Expression:

    def __init__(self, *operands):
        self.operands = operands
    
    def __add__(self, value):
        return Add(self, number_check(value))
    
    def __sub__(self, value):
        return Sub(self, number_check(value))
    
    def __mul__(self, value):
        return Mul(self, number_check(value))
    
    def __truediv__(self, value):
        return Div(self, number_check(value))
    
    def __pow__(self, value):
        return Pow(self, number_check(value))
    
    def __radd__(self, value):
        return Add(number_check(value), self)
    
    def __rsub__(self, value):
        return Sub(number_check(value), self)
    
    def __rmul__(self, value):
        return Mul(number_check(value), self)
    
    def __rtruediv__(self, value):
        return Div(number_check(value), self)
    
    def __rpow__(self, value):
        return Pow(number_check(value), self)

class Terminal(Expression):

    def __init__(self, value):
        self.value = value
        self.precedence = 0
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

    def __init__(self, *operands):
        newlisty = []
        for x in operands:
            newlisty.append(number_check(x))
        self.operands = tuple(newlisty)

    def __call__(self, symbol_map):
        return evaluatethis(self, symbol_map)

    def __repr__(self):
        return type(self).__name__ + repr(self.operands)
    
    def __str__(self):
        self.brackets = [[''] * 2] * 2
        for i in range(len(self.operands)):
            if self.operands[i].precedence > self.precedence:
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

@singledispatch
@evaluate.register(Number)
def _(expr, *o, **kwargs):
    return Number(expr.value)


@evaluate.register(Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return Number(symbol_map[expr.value])

@evaluate.register(int)
def _(expr, *o, **kwargs):
    return Number(expr)


@evaluate.register(Add)
def _(expr, *o, **kwargs):
    return Number(o[0] + o[1])


@evaluate.register(Sub)
def _(expr, *o, **kwargs):
    return Number(o[0] - o[1])


@evaluate.register(Mul)
def _(expr, *o, **kwargs):
    return Number(o[0] * o[1])


@evaluate.register(Div)
def _(expr, *o, **kwargs):
    return Number(o[0] / o[1])


@evaluate.register(Pow)
def _(expr, *o, **kwargs):
    return Number(o[0] ** o[1])


x = Symbol('x')
y = Symbol('y')
test1 = (3 * x + 2**(y / 5) - 1, 1.5, 10, 7.5)
test2 = (3 * x + 2**(y / 5) - 1, 2.5, 11, 11.09479341998814)
test3 = (4 * x + x**2 * y + 3 * y + 2, 1.0, 2.5, 16)
test4 = (4 * x + x**2 * y + 3 * y + 2, 1.1, 2.25, 15.8725)
test5 = x + 4
expr = 3*x + 2**(y/5) - 1

print(Add(Number(4), Number(3)))
print(test1[0]({'x' : 1.5, 'y' : 10}))
#print(postvisitor(expr, evaluate, symbol_map={'x': 1.5, 'y': 10}))

