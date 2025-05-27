class FPError(Exception):
    """Base class for all FP language errors"""
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_message())

    def format_message(self) -> str:
        if self.line is not None and self.column is not None:
            return f"Error at line {self.line}, column {self.column}: {self.message}"
        return f"Error: {self.message}"

class LexerError(FPError):
    """Raised when the lexer encounters an invalid character"""
    pass

class ParserError(FPError):
    """Raised when the parser encounters invalid syntax"""
    pass

class EvaluationError(FPError):
    """Raised when evaluation fails (e.g., type mismatch, undefined variable)"""
    pass

class TypeError(FPError):
    """Raised when an operation is performed on values of incompatible types"""
    pass
