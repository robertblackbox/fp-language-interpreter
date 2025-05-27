import argparse
import sys
from typing import Optional, TextIO
from .lexer import Lexer
from .parser import Parser
from .evaluator import Evaluator
from .env import Environment
from .error import FPError

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def run(self, source: str) -> str:
        try:
            # Tokenize the input
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            
            # Debug: Print tokens
            print("Tokens:", [f"{t.type}({t.value})" for t in tokens])

            # Parse tokens into ASTs
            parser = Parser(tokens)
            expressions = parser.parse()
            
            # Evaluate each expression in sequence
            result = None
            evaluator = Evaluator(None, self.env)  # Initialize with no AST
            for expr in expressions:
                evaluator.ast = expr  # Update AST for each expression
                result = evaluator.evaluate()
            
            # Format the result for better readability
            if result is None:
                return ""
            elif isinstance(result, list):
                return f"Result: [{', '.join(map(str, result))}]"
            elif isinstance(result, bool):
                return str(result).lower()
            elif isinstance(result, Function):
                return f"Function '{result.name if hasattr(result, 'name') else 'anonymous'}' defined"
            else:
                return str(result)
        except FPError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Internal error: {str(e)}"

def run_repl():
    """Run an interactive REPL (Read-Eval-Print Loop)"""
    interpreter = Interpreter()
    print("FP Language REPL (Ctrl+C to exit)")
    
    while True:
        try:
            # Read
            line = input("fp> ")
            if not line.strip():
                continue

            # Evaluate and Print
            result = interpreter.run(line)
            print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break

def run_file(file_path: str):
    """Run a source file"""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        
        interpreter = Interpreter()
        result = interpreter.run(source)
        print(result)

    except FileNotFoundError:
        print(f"Error: Could not find file '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="FP Language Interpreter")
    parser.add_argument("file", nargs="?", help="Path to source file")
    args = parser.parse_args()

    if args.file:
        run_file(args.file)
    else:
        run_repl()

if __name__ == "__main__":
    main()
