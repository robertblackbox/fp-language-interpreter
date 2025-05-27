from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class Node:
    def __str__(self) -> str:
        return self.__repr__()

@dataclass
class Number(Node):
    value: int
    
    def __str__(self) -> str:
        return str(self.value)

@dataclass
class Identifier(Node):
    name: str
    
    def __str__(self) -> str:
        return self.name

@dataclass
class BinaryOp(Node):
    left: Node
    operator: str
    right: Node
    
    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

@dataclass
class FunctionDef(Node):
    name: str
    params: List[str]
    body: Node
    
    def __str__(self) -> str:
        params_str = ", ".join(self.params)
        return f"def {self.name}({params_str}) = {self.body}"

@dataclass
class FunctionCall(Node):
    name: str
    arguments: List[Node]
    
    def __str__(self) -> str:
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"{self.name}({args_str})"

@dataclass
class IfExpr(Node):
    condition: Node
    then_branch: Node
    else_branch: Node
    
    def __str__(self) -> str:
        return f"if {self.condition} then {self.then_branch} else {self.else_branch}"

@dataclass
class LetBinding(Node):
    name: str
    value: Node
    body: Node
    
    def __str__(self) -> str:
        return f"let {self.name} = {self.value} in {self.body}"

@dataclass
class List(Node):
    elements: List[Node]
    
    def __str__(self) -> str:
        elems_str = ", ".join(str(elem) for elem in self.elements)
        return f"[{elems_str}]"

# Built-in functions for list operations
@dataclass
class Head(Node):
    list_expr: Node
    
    def __str__(self) -> str:
        return f"head({self.list_expr})"

@dataclass
class Tail(Node):
    list_expr: Node
    
    def __str__(self) -> str:
        return f"tail({self.list_expr})"

@dataclass
class Length(Node):
    list_expr: Node
    
    def __str__(self) -> str:
        return f"length({self.list_expr})"

@dataclass
class Concat(Node):
    left: Node
    right: Node
    
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"
