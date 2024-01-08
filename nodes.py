import operator
import math
import ast
import itertools

from .registry import register_node, scrape_module
from .types import *


binary_ops = {v.__name__: v for v in itertools.chain(
    scrape_module(operator, 2),
    scrape_module(math, 2),
)}


@register_node(display_name="Binary Operation")
def BinaryOp(a: Any, b: Any, operation: Combo(choices=binary_ops) = 'add') -> (Any, ):
    return (operation(a, b), )


@register_node(display_name="Mapped Binary Operation")
def MappedBinaryOp(iterable: 'ITER', operation: Combo(choices=binary_ops) = 'add') -> ('ITER', ):
    return (itertools.starmap(operation, iterable), )


unary_ops = {v.__name__: v for v in itertools.chain(
    scrape_module(operator, 1),
    scrape_module(math, 1),
)}


@register_node(display_name="Unary Operation")
def UnaryOp(a: Any, operation: Combo(choices=unary_ops) = 'sqrt') -> (Any, ):
    return (operation(a), )


@register_node(display_name="Mapped Unary Operation")
def MappedUnaryOp(iterable: 'ITER', operation: Combo(choices=unary_ops) = 'sqrt') -> ('ITER', ):
    return (map(operation, iterable), )


@register_node()
def Join(iterable: 'ITER', sep: String() = ", ") -> (String(), ):
    return (sep.join(str(x) for x in iterable))


@register_node(display_name="Mapped Join")
def MapJoin(iterable: 'ITER', sep: String() = ", ") -> ('ITER', ):
    return (itertools.starmap(sep.join, iterable), )


@register_node(output=True)
def Print(a: Any, mode: Combo(choices={'str': str, 'repr': repr}) = 'str') -> ():
    #print(mode(a))
    return ()


@register_node()
def Literal(code: String(multiline=True) = "") -> (Any, ):
    #print(code)
    return (ast.literal_eval(code), )


@register_node(display_name="Get Item")
def GetItem(collection: 'COLLECTION', item: Any) -> (Any, ):
    return (collection[item], )


format_modes = {
    'mapping': lambda x, y: x.format(**y),
    'iterable': lambda x, y: x.format(*y),
    'single': lambda x, y: x.format(y)
}

@register_node()
def Format(vars: Any, string: String(multiline=True) = "", mode: Combo(choices=format_modes) = 'mapping') -> (String(), ):
    return (mode(string, vars), )


