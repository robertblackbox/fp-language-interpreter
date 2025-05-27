# FP Language Interpreter

A simple functional programming language interpreter implemented in Python. The language supports:
- Immutable variables
- First-class functions
- Recursion
- List operations
- Basic arithmetic and comparison operations

## Features

- **Functional Programming Paradigm**: Pure functions, immutability, and recursion
- **Built-in List Operations**: head, tail, length
- **Control Flow**: if-then-else expressions
- **Variable Bindings**: let expressions
- **Function Definitions**: with multiple parameters
- **Error Handling**: Detailed error messages with line and column information

## Example: Bubble Sort Implementation

```fp
// Helper function to perform one pass of bubble sort
def bubblePass(lst) = 
    if length(lst) < 2 then 
        (lst, false)
    else {
        let first = head(lst)
        let rest = tail(lst)
        let (sorted_rest, swapped) = bubblePass(rest)
        let next = head(sorted_rest)
        
        if first > next then
            ([next] + [first] + tail(sorted_rest), true)
        else
            ([first] + sorted_rest, swapped)
    }

// Main bubble sort function
def bubbleSort(lst) = {
    let (new_lst, swapped) = bubblePass(lst)
    if swapped then
        bubbleSort(new_lst)
    else
        new_lst
}

// Test
let test_list = [64, 34, 25, 12, 22, 11, 90]
bubbleSort(test_list)  // Returns [11, 12, 22, 25, 34, 64, 90]
```

## Usage

### Running the Interpreter

1. **REPL Mode** (Interactive):
   ```bash
   python -m fp_lang.interpreter
   ```

2. **File Mode**:
   ```bash
   python -m fp_lang.interpreter path/to/your/script.fp
   ```

### Language Syntax

1. **Variable Binding**:
   ```fp
   let x = 5
   x + 3  // Returns 8
   ```

2. **Function Definition**:
   ```fp
   def add(x, y) = x + y
   add(2, 3)  // Returns 5
   ```

3. **Conditional Expression**:
   ```fp
   if x > 0 then 
       "positive" 
   else 
       "non-positive"
   ```

4. **List Operations**:
   ```fp
   let lst = [1, 2, 3]
   head(lst)     // Returns 1
   tail(lst)     // Returns [2, 3]
   length(lst)   // Returns 3
   ```

## Running Tests

To run the test suite:

```bash
python -m unittest fp_lang/tests/test_interpreter.py
```

## Implementation Details

The interpreter is implemented with the following components:

1. **Lexer** (`lexer.py`): Tokenizes the input source code
2. **Parser** (`parser.py`): Converts tokens into an Abstract Syntax Tree (AST)
3. **AST Nodes** (`ast_nodes.py`): Defines the structure of the AST
4. **Environment** (`env.py`): Manages variable scope and bindings
5. **Evaluator** (`evaluator.py`): Executes the AST
6. **Error Handling** (`error.py`): Provides detailed error messages

## Error Handling

The interpreter provides detailed error messages including:
- Syntax errors with line and column information
- Runtime errors (type mismatches, undefined variables)
- Stack traces for debugging

## Contributing

Feel free to contribute by:
1. Opening issues for bugs or feature requests
2. Submitting pull requests with improvements
3. Adding more example programs
4. Improving documentation

## License

MIT License - feel free to use this code for any purpose.
