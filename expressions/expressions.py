import numbers
from functools import wraps

def make_other_expr(meth):
    """Cast the second argument of a method to Number when needed."""
    @wraps(meth)
    def fn(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return meth(self, other)
    return fn

def postvisitor(expr, fn, **kwargs):
    newstack = [expr]
    visited = {}
    while len(newstack) > 0:
        curr = newstack.pop()
        unvisited = []
        if isinstance(curr, Operator):
            for elem in curr.operands:
                if elem not in visited:
                    unvisited.append(elem)
        if len(unvisited) > 0:
            newstack.append(curr)
            for elem in unvisited:
                newstack.append(elem)
        else:
            if isinstance(curr, Operator):
                visited[curr] = fn(curr, *(visited[elem] for elem in curr.operands))
            else:
                visited[curr] = fn(curr, **kwargs)
    
    return visited[expr]

def ifnumber(value):
    if isinstance(value, numbers.Number):
        return Number(value)
    else:
        return value

class Expression:
    def __init__(self, *operands):
        self.operands = operands

    @make_other_expr
    def __add__(self, value):
        return Add(self, value)

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


@evaluate.register(Number)
def _(expr, *o, **kwargs):
    return expr.value


@evaluate.register(Symbol)
def _(expr, *o, symbol_map, **kwargs):
    return symbol_map[expr.value]


@evaluate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@evaluate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@evaluate.register(Mul)
def _(expr, *o, **kwargs):
    return o[0] * o[1]


@evaluate.register(Div)
def _(expr, *o, **kwargs):
    return o[0] / o[1]


@evaluate.register(Pow)
def _(expr, *o, **kwargs):
    return o[0] ** o[1]


@singledispatch
def differentiate(expr, var, *o, **kwargs):
    """Differentiate!!"""

    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, var, *o, **kwargs):
    return Number(0)


@differentiate.register(Symbol)
def _(expr, var, *o, **kwargs):
    if expr.value == var:
        return Number(1)
    else:
        return Number(0)


@differentiate.register(Add)
def _(expr, var, *o, **kwargs):
    curr = expr.operands
    return differentiate(curr[0], var, **kwargs) + differentiate(curr[1], var, **kwargs)


@differentiate.register(Sub)
def _(expr, var, *o, **kwargs):
    curr = expr.operands
    return differentiate(curr[0], var, **kwargs) - differentiate(curr[1], var, **kwargs)


@differentiate.register(Mul)
def _(expr, var, *o, **kwargs):
    curr = expr.operands
    return curr[0]*differentiate(curr[1], var, **kwargs) + differentiate(curr[0], var, **kwargs)*curr[1]


@differentiate.register(Div)
def _(expr, var, *o, **kwargs):
    return differentiate(o[0] * (o[1] ** (-1)), var, **kwargs)


@differentiate.register(Pow)
def _(expr, var, *o, **kwargs):
    curr = expr.operands
    if isinstance(curr[0], Expression):
        if ((isinstance(curr[0], Symbol) and curr[0].value == var) or (isinstance(curr[0], Operator))):
            return curr[1] * curr[0] ** (curr[1] - 1)
        elif ((isinstance(curr[1], Symbol) and curr[1].value == var) or (isinstance(curr[1], Operator))):
            raise NotImplementedError("Wth...")
    else:
        return curr[0] ** curr[1]


x = Symbol('x')
y = Symbol('y')

expr = x**5

print(differentiate(expr, 'x'))
