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
    """All binary operators from Python stdlib."""
    return (operation(a, b), )


@register_node(display_name="Mapped Binary Operation")
def MappedBinaryOp(iterable: 'ITER', operation: Combo(choices=binary_ops) = 'add') -> ('ITER', ):
    """Map a binary operation to an iterable."""
    return (itertools.starmap(operation, iterable), )


unary_ops = {v.__name__: v for v in itertools.chain(
    scrape_module(operator, 1),
    scrape_module(math, 1),
)}


@register_node(display_name="Unary Operation")
def UnaryOp(a: Any, operation: Combo(choices=unary_ops) = 'sqrt') -> (Any, ):
    """All unary operators from Python stdlib."""
    return (operation(a), )


@register_node(display_name="Mapped Unary Operation")
def MappedUnaryOp(iterable: 'ITER', operation: Combo(choices=unary_ops) = 'sqrt') -> ('ITER', ):
    """Map a unary operation to an iterable."""
    return (map(operation, iterable), )


@register_node()
def Join(iterable: 'ITER', sep: String() = ", ") -> (String(), ):
    """Joins an interable of strings into a single string."""
    return (sep.join(str(x) for x in iterable))


@register_node(display_name="Mapped Join")
def MapJoin(iterable: 'ITER', sep: String() = ", ") -> ('ITER', ):
    """I can't remember what this does. :("""
    return (itertools.starmap(sep.join, iterable), )


@register_node(output=True)
def Print(a: Any, mode: Combo(choices={'str': str, 'repr': repr}) = 'str') -> ():
    """Prints the str() or repr() of the input."""
    print(mode(a))
    return ()


@register_node()
def Literal(code: String(multiline=True) = "") -> (Any, ):
    """Allows defining a literal value directly in Python code."""
    return (ast.literal_eval(code), )


@register_node(display_name="Get Item")
def GetItem(collection: 'COLLECTION', item: Any) -> (Any, ):
    """Selects a key from a collection ie a dict."""
    return (collection[item], )


format_modes = {
    'mapping': lambda x, y: x.format(**y),
    'iterable': lambda x, y: x.format(*y),
    'single': lambda x, y: x.format(y)
}

@register_node()
def Format(vars: Any, string: String(multiline=True) = "", mode: Combo(choices=format_modes) = 'mapping') -> (String(), ):
    """Performs string replacement using the standard Python format() method."""
    return (mode(string, vars), )


@register_node()
def Switch(a: Any, b: Any, select: Bool(label_on="A", label_off="B") = True) ->(Any, ):
    """A switch that selects between the two inputs."""
    return (a if select else b, )
