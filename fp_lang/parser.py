from typing import Optional, Sequence
from typing import List as TypeList
from .lexer import Token, TokenType
from .ast_nodes import *

class Parser:
    def __init__(self, tokens: Sequence[Token]):
        self.tokens = tokens
        self.current = 0

    def error(self, message: str):
        token = self.current_token()
        raise Exception(f"{message} at line {token.line}, column {token.column}")

    def current_token(self) -> Token:
        return self.tokens[self.current]

    def peek(self) -> Token:
        if self.current + 1 >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.current + 1]

    def advance(self):
        self.current += 1

    def consume(self, type: TokenType, message: str):
        if self.current_token().type == type:
            self.advance()
        else:
            self.error(message)

    def parse(self) -> TypeList[Node]:
        # Parse a sequence of expressions
        expressions = []
        while self.current < len(self.tokens) and self.current_token().type != TokenType.EOF:
            expr = self.expression()
            if expr is not None:
                expressions.append(expr)
        return expressions

    def expression(self) -> Node:
        if self.current_token().type == TokenType.DEF:
            return self.function_definition()
        elif self.current_token().type == TokenType.LET:
            return self.let_binding()
        elif self.current_token().type == TokenType.IF:
            return self.if_expression()
        elif self.current_token().type == TokenType.LBRACE:
            return self.block_expression()
        return self.comparison()

    def block_expression(self) -> Node:
        """Parse a block of expressions enclosed in curly braces"""
        self.consume(TokenType.LBRACE, "Expected '{'")
        expressions = []
        
        while self.current_token().type != TokenType.RBRACE:
            expressions.append(self.expression())
            
        self.consume(TokenType.RBRACE, "Expected '}'")
        
        # Return the last expression in the block
        if not expressions:
            self.error("Empty block")
        return expressions[-1]

    def function_definition(self) -> Node:
        self.consume(TokenType.DEF, "Expected 'def'")
        if self.current_token().type != TokenType.IDENTIFIER:
            self.error("Expected function name")
        name = self.current_token().value
        self.advance()

        self.consume(TokenType.LPAREN, "Expected '('")
        params = []
        while self.current_token().type != TokenType.RPAREN:
            if self.current_token().type != TokenType.IDENTIFIER:
                self.error("Expected parameter name")
            params.append(self.current_token().value)
            self.advance()
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.consume(TokenType.RPAREN, "Expected ')'")
        
        self.consume(TokenType.EQ, "Expected '='")
        body = self.expression()
        return FunctionDef(name, params, body)

    def let_binding(self) -> Node:
        self.consume(TokenType.LET, "Expected 'let'")
        
        # Handle tuple destructuring
        if self.current_token().type == TokenType.LPAREN:
            self.advance()
            names = []
            while self.current_token().type != TokenType.RPAREN:
                if self.current_token().type != TokenType.IDENTIFIER:
                    self.error("Expected identifier in tuple destructuring")
                names.append(self.current_token().value)
                self.advance()
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
            self.consume(TokenType.RPAREN, "Expected ')'")
            
            self.consume(TokenType.EQ, "Expected '='")
            value = self.expression()
            
            # Create nested let bindings for tuple destructuring
            body = self.expression()
            for i, name in reversed(list(enumerate(names))):
                # For each name, create a let binding that extracts the corresponding element
                # from the tuple using list indexing
                index_expr = Number(i)
                value_expr = FunctionCall("get_tuple_element", [Identifier("_tuple"), index_expr])
                body = LetBinding(name, value_expr, body)
            
            # Wrap everything in a let binding for the tuple itself
            return LetBinding("_tuple", value, body)
            
        else:
            # Regular let binding
            if self.current_token().type != TokenType.IDENTIFIER:
                self.error("Expected identifier after 'let'")
            name = self.current_token().value
            self.advance()
            
            self.consume(TokenType.EQ, "Expected '='")
            value = self.expression()
            return LetBinding(name, value, self.expression())

    def if_expression(self) -> Node:
        self.consume(TokenType.IF, "Expected 'if'")
        condition = self.expression()
        self.consume(TokenType.THEN, "Expected 'then'")
        then_branch = self.expression()
        self.consume(TokenType.ELSE, "Expected 'else'")
        else_branch = self.expression()
        return IfExpr(condition, then_branch, else_branch)

    def comparison(self) -> Node:
        node = self.term()
        
        while self.current_token().type in [TokenType.GT, TokenType.LT, TokenType.EQ]:
            op = self.current_token().value
            self.advance()
            right = self.term()
            node = BinaryOp(node, op, right)
            
        return node

    def term(self) -> Node:
        node = self.factor()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.factor()
            node = BinaryOp(node, op, right)
            
        return node

    def factor(self) -> Node:
        node = self.primary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token().value
            self.advance()
            right = self.primary()
            node = BinaryOp(node, op, right)
            
        return node

    def primary(self) -> Node:
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(int(token.value))
        elif token.type == TokenType.TRUE:
            self.advance()
            return Number(1)  # Represent true as 1
        elif token.type == TokenType.FALSE:
            self.advance()
            return Number(0)  # Represent false as 0
            
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current_token().type != TokenType.RPAREN:
                    args.append(self.expression())
                    if self.current_token().type == TokenType.COMMA:
                        self.advance()
                self.consume(TokenType.RPAREN, "Expected ')'")
                return FunctionCall(token.value, args)
            return Identifier(token.value)
            
        elif token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            while self.current_token().type != TokenType.RBRACKET:
                elements.append(self.expression())
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
            self.consume(TokenType.RBRACKET, "Expected ']'")
            return List(elements)
            
        elif token.type == TokenType.LPAREN:
            self.advance()
            # Check if it's a tuple
            expressions = [self.expression()]
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                expressions.append(self.expression())
            self.consume(TokenType.RPAREN, "Expected ')'")
            # If there's only one expression, it's just parentheses
            if len(expressions) == 1:
                return expressions[0]
            # Otherwise, it's a tuple
            return List(expressions)  # Using List node for tuples
            
        self.error(f"Unexpected token: {token.value}")
