import unittest
from ..lexer import Lexer
from ..parser import Parser
from ..evaluator import Evaluator
from ..env import Environment
from ..interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_basic_arithmetic(self):
        tests = [
            ("1 + 2", "3"),
            ("3 * 4", "12"),
            ("10 - 5", "5"),
            ("8 / 2", "4.0"),
        ]
        
        for source, expected in tests:
            result = self.interpreter.run(source)
            self.assertEqual(result, expected)

    def test_comparison(self):
        tests = [
            ("1 < 2", "True"),
            ("3 > 2", "True"),
            ("2 = 2", "True"),
            ("1 = 2", "False"),
        ]
        
        for source, expected in tests:
            result = self.interpreter.run(source)
            self.assertEqual(result, expected)

    def test_if_expression(self):
        source = """
        if 1 < 2 then 
            10 
        else 
            20
        """
        result = self.interpreter.run(source)
        self.assertEqual(result, "10")

    def test_let_binding(self):
        source = """
        let x = 5
        x + 3
        """
        result = self.interpreter.run(source)
        self.assertEqual(result, "8")

    def test_function_definition_and_call(self):
        source = """
        def add(x, y) = x + y
        add(2, 3)
        """
        result = self.interpreter.run(source)
        self.assertEqual(result, "5")

    def test_list_operations(self):
        tests = [
            ("[1, 2, 3]", "[1, 2, 3]"),
            ("head([1, 2, 3])", "1"),
            ("tail([1, 2, 3])", "[2, 3]"),
            ("length([1, 2, 3])", "3"),
        ]
        
        for source, expected in tests:
            result = self.interpreter.run(source)
            self.assertEqual(result, expected)

    def test_bubble_sort(self):
        # Test the complete bubble sort implementation
        with open('fp_lang/examples/bubble_sort.fp', 'r') as f:
            source = f.read()
        
        result = self.interpreter.run(source)
        self.assertEqual(result, "[11, 12, 22, 25, 34, 64, 90]")

if __name__ == '__main__':
    unittest.main()
