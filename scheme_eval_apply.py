import sys

from CS078.Scheme_Interpreter.link import *
from CS078.Scheme_Interpreter.scheme_utils import *
from CS078.Scheme_Interpreter.scheme_reader import read_line
from CS078.Scheme_Interpreter.scheme_builtins import create_global_frame
from CS078.Scheme_Interpreter.ucb import main, trace

"""
scheme_eval_apply.py
COMSC-078
Contributors:
  Thomas: Problem 2
  Thalia: Problem 3
  Melika: Problem 6
  Melika: Problem 9
  Zeenia: Problem 11
  Chris: Debug Problem 6: fixed duplicate eval_all definition

Core evaluator and apply logic for the Scheme interpreter.
Implements recursive eval/apply cycle for expressions, built-in
procedures, lambda procedures, and dynamically scoped mu procedures.
"""


def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Link('+', Link(2, Link(2)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    if not scheme_listp(expr):
        raise SchemeError("malformed list: {0}".format(repl_str(expr)))
    first, rest = expr.first, expr.rest

    from CS078.Scheme_Interpreter.scheme_forms import (
        SPECIAL_FORMS,
    )  # Import here to avoid a cycle when modules are loaded

    if scheme_symbolp(first) and first in SPECIAL_FORMS:
        return SPECIAL_FORMS[first](rest, env)
    else:
        # BEGIN PROBLEM 3
        operator = scheme_eval(first, env)
        operands = rest.map(lambda x: scheme_eval(x, env))
        return scheme_apply(operator, operands, env)
        # END PROBLEM 3


def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
        assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        py_args = []
        link = args
        while link is not Link.empty:
            py_args.append(link.first)
            link = link.rest
        if procedure.need_env:
            py_args.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            return procedure.py_func(*py_args)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError("incorrect number of arguments: {0}".format(procedure))
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        # Create a new environment where the lambda was defined
        new_env = procedure.env.make_child_frame(procedure.formals, args)
        # Evaluate the body of the procedure in the new environment
        return eval_all(procedure.body, new_env)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        new_env = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, new_env)
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)


    # BEGIN Problem 6
def eval_all(expressions, env):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last."""
    # If there are no expressions, return None (undefined)
    if expressions is Link.empty:
        return None
    # Evaluate expressions sequentially
    result = None
    while expressions is not Link.empty:
        result = scheme_eval(expressions.first, env)
        expressions = expressions.rest
    return result
    # END PROBLEM 6


###################################
# Extra Challenge: Tail Recursion #
###################################


class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val


def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""

    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 2
        # END OPTIONAL PROBLEM 2

    return optimized_eval


################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

# scheme_eval = optimize_tail_calls(scheme_eval)
