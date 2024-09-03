"""
File Purpose: math tools
"""

import ast
import math
import operator as op

import numpy as np

''' --------------------- ast math eval --------------------- '''

def ast_math_eval(expr):
    '''evaluate a string math expression using ast. (only accepts numbers & math operations.)
    This is safe because it uses ast; it does not ever use the unsafe eval() command.
    '''
    node = ast.parse(expr, mode='eval').body
    return _ast_math_eval_node(node)

# dict of {ast class: associated operator}
AST_OPS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        }

def _ast_math_eval_node(node):
    '''evaluate a parsed ast node, recursively. For internal use. See ast_math_eval() for user interface.'''
    if isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.BinOp):
        this_op = AST_OPS[type(node.op)]
        return this_op(_ast_math_eval_node(node.left), _ast_math_eval_node(node.right))
    elif isinstance(node, ast.UnaryOp):
        this_op = AST_OPS[type(node.op)]
        return this_op(_ast_math_eval_node(node.operand))
    else:
        raise TypeError(node)


''' --------------------- rounding --------------------- '''

def round_to_int(x, mode='round'):
    '''return x rounded to an integer, using the specified mode.
    (if x is already an integer, returns x unchanged.)

    mode: 'round', 'floor', 'ceil' or 'int'
        'round' --> as per builtins.round(). round to nearest integer, ties toward even integers.
        'int' --> as per builtins.int(). always rounds towards 0.
        'floor' --> round towards negative infinity.
        'ceil' --> round towards positive infinity.
    '''
    if mode == 'round':
        return round(x)
    elif mode == 'int':
        return int(x)
    elif mode == 'floor':
        return math.floor(x)
    elif mode == 'ceil':
        return math.ceil(x)
    else:
        raise ValueError(f'unrecognized mode={mode!r}, expected "round", "int", "floor", or "ceil".')

def float_rounding(x, prec=8):
    '''round x to a more-likely-to-be-input float (if possible, else just return x).
    [TODO] change this to work even if a decimal point appears inside the 0's or 9's.

    Examples:
        0.20000000001, prec=8 --> float(0.2)
        35999999999.0, prec=8 --> float(36000000000)
        35999999999.0, prec=12 --> unchanged (because prec > number of consecutive 0's or 9's)
        0.12345678901234 --> unchanged (because no sequence of consecutive 0's or 9's)

    prec: int
        number of consecutive 0's or 9's required in str(x) before rounding.
    '''
    s = str(float(x))
    round0str = '0' * prec
    round9str = '9' * prec
    if round0str in s:
        i = s.index(round0str)
        result, remaining = s[:i], s[i:]
    elif round9str in s:
        i = s.index(round9str)
        if i == 0:
            return x  # no rounding needed, x just starts like 9999999...
        result, remaining = s[:i], s[i:]
        result = result[:-1] + str(int(result[-1]) + 1)  # add 1 to final digit; we are rounding it up.
    else:
        return x  # no obvious rounding to do.
    if '.' in remaining:  # we are before the decimal point.
        d = remaining.index('.')
        result += '0' * d   # append enough 0's to reach the decimal point.
        if 'e' in remaining:  # if e follows, append the exponent. (probably never used)
            e = remaining.index('e')
            result += remaining[e:]
    elif 'e' in remaining:  # we are before the exponent and also before the decimal point. (probably never used)
        e = remaining.index('e')
        result += '0' * e + remaining[e:] # append the appropriate number of 0's, then the exponent.
    return float(result)


''' --------------------- classify math objects --------------------- '''

def is_integer(x):
    '''return whether x is an integer.
    by first checking isinstance(x, int),
    if that's False, check x.is_integer() if it exists,
    else return False.
    '''
    if isinstance(x, int):
        return True
    else:
        try:
            return x.is_integer()
        except AttributeError:
            return False


''' --------------------- numpy math --------------------- '''

def np_all_int(x):
    '''returns whether all values in x are integer-valued. (regardless of x's type).
    Equivalent: np.all(np.mod(x, 1) == 0)
    '''
    return np.all(np.equal(np.mod(x, 1), 0))
