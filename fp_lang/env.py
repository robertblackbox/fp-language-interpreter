from typing import Dict, Any, Optional
from dataclasses import dataclass
from .ast_nodes import Node

@dataclass
class Function:
    params: list[str]
    body: Node
    env: 'Environment'

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent

    def define(self, name: str, value: Any):
        """Define a new variable in the current scope"""
        self.values[name] = value

    def assign(self, name: str, value: Any):
        """
        Assign a value to an existing variable in the current or parent scope
        Raises an error if the variable doesn't exist (enforcing immutability)
        """
        if name in self.values:
            self.values[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"Variable '{name}' is not defined")

    def get(self, name: str) -> Any:
        """Get the value of a variable from the current or parent scope"""
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Variable '{name}' is not defined")

    def extend(self) -> 'Environment':
        """Create a new child environment"""
        return Environment(self)
