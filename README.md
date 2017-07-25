# Implementation of an Interpreter

## Phases of a Simple Interpreter
### Scanning
The scanner reads a source program as a text file and produces a stream of tokens.

### Parsing
The parser processes tokens produced by the scanner, determines the syntactic validity of the token stream, and creates an abstract syntax tree (AST) suitable for the compiler’s subsequent activities.

### Symbol Table
The AST created by the parsing task is next traversed to create a symbol table. This table associates type and other contextual information with variables used in an program.

### Semantic Analysis
The AST is next traversed to perform semantic analysis. Semantic analysis often decorates or transforms portions of an AST as the actual meaning of such portions becomes more clear. For example, an AST node for the + operator may be replaced with the actual meaning of +, which may mean floating point or integer addition.

### Code Generation
Finally, the AST is traversed to generate a translation of the original program, i.e. code for a virtual machine.

## References
1. [Charles N. Fischer et al, Crafting a Compiler, 2009](https://www.pearsonhighered.com/program/Fischer-Crafting-A-Compiler/PGM315544.html)
2. [Ronald Mak, Writing Compilers and Interpreters: A Software Engineering Approach, 3rd Edition](https://www.amazon.com/Writing-Compilers-Interpreters-Software-Engineering/dp/0470177071)
3. [Terence Parr, Language Implementation Patterns: Create Your Own Domain-Specific and General Programming Languages, 2010](https://pragprog.com/book/tpdsl/language-implementation-patterns)
4. [Keith D. Cooper et al, Engineering a Compiler, 2nd Edition](http://www.cs.rice.edu/~keith/)
5. [Ruslan Spivak, Let's Build a Simple Interpreter](https://github.com/rspivak/lsbasi)
