from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"
    DEF = "DEF"
    LET = "LET"
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    GT = "GT"
    LT = "LT"
    EQ = "EQ"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None

    def error(self):
        raise Exception(f'Invalid character {self.current_char} at line {self.line}, column {self.column}')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.source) - 1:
            self.current_char = None
        else:
            self.current_char = self.source[self.pos]
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def identifier(self):
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/':
                if self.peek() == '/':
                    self.advance()  # Skip first /
                    self.advance()  # Skip second /
                    self.skip_comment()
                    continue
                else:
                    self.advance()
                    return Token(TokenType.DIVIDE, '/', self.line, self.column)

            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, str(self.number()), self.line, self.column)

            if self.current_char.isalpha():
                identifier = self.identifier()
                if identifier == 'def':
                    return Token(TokenType.DEF, identifier, self.line, self.column)
                elif identifier == 'let':
                    return Token(TokenType.LET, identifier, self.line, self.column)
                elif identifier == 'if':
                    return Token(TokenType.IF, identifier, self.line, self.column)
                elif identifier == 'then':
                    return Token(TokenType.THEN, identifier, self.line, self.column)
                elif identifier == 'else':
                    return Token(TokenType.ELSE, identifier, self.line, self.column)
                elif identifier == 'true':
                    return Token(TokenType.TRUE, identifier, self.line, self.column)
                elif identifier == 'false':
                    return Token(TokenType.FALSE, identifier, self.line, self.column)
                return Token(TokenType.IDENTIFIER, identifier, self.line, self.column)

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.column)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.column)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MULTIPLY, '*', self.line, self.column)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, self.column)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.column)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.column)

            if self.current_char == '[':
                self.advance()
                return Token(TokenType.LBRACKET, '[', self.line, self.column)

            if self.current_char == ']':
                self.advance()
                return Token(TokenType.RBRACKET, ']', self.line, self.column)

            if self.current_char == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, self.column)

            if self.current_char == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, self.column)

            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, self.column)

            if self.current_char == '>':
                self.advance()
                return Token(TokenType.GT, '>', self.line, self.column)

            if self.current_char == '<':
                self.advance()
                return Token(TokenType.LT, '<', self.line, self.column)

            if self.current_char == '=':
                self.advance()
                return Token(TokenType.EQ, '=', self.line, self.column)

            self.error()

        return Token(TokenType.EOF, '', self.line, self.column)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.source) - 1:
            return None
        return self.source[peek_pos]

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens
