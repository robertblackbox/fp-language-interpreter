from typing import Any, List
from .ast_nodes import *
from .env import Environment, Function

class Evaluator:
    def __init__(self, ast: Node, env: Environment):
        self.ast = ast
        self.env = env
        self._setup_builtins()

    def _setup_builtins(self):
        """Set up built-in functions in the environment"""
        def head(lst):
            if not isinstance(lst, list) or len(lst) == 0:
                raise ValueError("head: empty list")
            return lst[0]

        def tail(lst):
            if not isinstance(lst, list) or len(lst) == 0:
                raise ValueError("tail: empty list")
            return lst[1:]

        def length(lst):
            if not isinstance(lst, list):
                raise ValueError("length: not a list")
            return len(lst)

        def get_tuple_element(tuple_val, index):
            if not isinstance(tuple_val, list):
                raise ValueError("get_tuple_element: not a tuple")
            if not isinstance(index, int):
                raise ValueError("get_tuple_element: index must be a number")
            if index < 0 or index >= len(tuple_val):
                raise ValueError("get_tuple_element: index out of bounds")
            return tuple_val[index]

        self.env.define("head", head)
        self.env.define("tail", tail)
        self.env.define("length", length)
        self.env.define("get_tuple_element", get_tuple_element)

    def evaluate(self) -> Any:
        """Evaluate the AST and return the result"""
        return self._eval(self.ast, self.env)

    def _eval(self, node: Node, env: Environment) -> Any:
        try:
            # Numbers evaluate to themselves
            if isinstance(node, Number):
                return node.value

            # Variable lookup
            if isinstance(node, Identifier):
                return env.get(node.name)

            # Binary operations
            if isinstance(node, BinaryOp):
                left = self._eval(node.left, env)
                right = self._eval(node.right, env)
                
                if node.operator == '+':
                    if isinstance(left, list) and isinstance(right, list):
                        return left + right
                    return left + right
                elif node.operator == '-':
                    return left - right
                elif node.operator == '*':
                    return left * right
                elif node.operator == '/':
                    return left / right
                elif node.operator == '>':
                    return bool(left > right)
                elif node.operator == '<':
                    return bool(left < right)
                elif node.operator == '=':
                    return bool(left == right)
                else:
                    raise ValueError(f"Unknown operator: {node.operator}")

            # Function definition
            if isinstance(node, FunctionDef):
                function = Function(node.params, node.body, env)
                env.define(node.name, function)
                return function

            # Function call
            if isinstance(node, FunctionCall):
                function = env.get(node.name)
                if isinstance(function, Function):
                    # Evaluate arguments
                    args = [self._eval(arg, env) for arg in node.arguments]
                    
                    # Create new environment for function execution
                    new_env = function.env.extend()
                    
                    # Bind parameters to arguments
                    for param, arg in zip(function.params, args):
                        new_env.define(param, arg)
                    
                    # Execute function body in new environment
                    return self._eval(function.body, new_env)
                elif callable(function):
                    # Handle built-in functions
                    args = [self._eval(arg, env) for arg in node.arguments]
                    return function(*args)
                else:
                    raise ValueError(f"'{node.name}' is not a function")

            # If expression
            if isinstance(node, IfExpr):
                condition = bool(self._eval(node.condition, env))
                if condition:
                    return self._eval(node.then_branch, env)
                else:
                    return self._eval(node.else_branch, env)

            # Let binding
            if isinstance(node, LetBinding):
                value = self._eval(node.value, env)
                new_env = env.extend()
                new_env.define(node.name, value)
                return self._eval(node.body, new_env)

            # List literal
            if isinstance(node, List):
                return [self._eval(elem, env) for elem in node.elements]

            raise ValueError(f"Unknown node type: {type(node)}")
        except Exception as e:
            raise ValueError(f"Evaluation error at {node}: {str(e)}")
