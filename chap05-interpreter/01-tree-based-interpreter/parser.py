###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     statements ::= assignment * returnstmt ?
#     returnstmt ::= 'return' expression
#     assignment ::= identifier '=' expression | 'function' identifier definition
#     expression ::= term (('+'|'-') term)* | function
#     arguments ::= (expression(',' expression)*)?
#     function ::= 'function' definition 
#     definition ::= '(' parameters ')' statements 'end'
#     parameters ::= (identifier(',' identifier)*) ?
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer | ('+'|'-') factor | prefixexp
#     ( or factor ::= ('+'|'-')* (integer | prefixexp) )
#     prefixexp ::= (identifier | '(' expression ')') ('(' arguments ')')*
#     integer ::= digit +
#     identifier ::= letter (letter | digit) *
###########################################################

###########################################################
# CharStream -- an input stream of characters
###########################################################
class CharStream:
    def __init__(self, text):
        self.text = text     # source code
        self.position = -1   # current position
        self.nextChar()

    def nextChar(self):
        '''
        Consume the current source character and return the next character.
        '''
        if self.position + 1 < len(self.text):
            self.position += 1
            self.currentChar = self.text[self.position]
        else:
            self.currentChar = None

    def skipWhiteSpace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.nextChar()

###########################################################
# Token
###########################################################
# Token types
INTEGER, PLUS, MINUS, MUL, DIV,          \
LPAREN, RPAREN, IDENTIFIER, ASSIGN, EOF, \
COMMA, FUNCTION, END, RETURN = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV',
    'LPAREN', 'RPAREN', 'IDENTIFIER', 'ASSIGN', 'EOF',
    'COMMA', 'FUNCTION', 'END', 'RETURN',
    )

# Phony token types -- Used in creating AST nodes that don't derived from tokens
# So, we can get node type va token.type
STATEMENTS, ARGUMENTS, PARAMETERS, CALL, DEFINE = (
    'STATEMENTS', 'ARGUMENTS', 'PARAMETERS', 'CALL', 'DEFINE')

class Token:
    def __init__(self, type, text, position):
        self.type = type         # token type
        self.text = text         # token text
        self.position = position # position of the first token character

    def __str__(self):
        return '{type}({position}): {text}'.format(
            position = self.position,
            type = self.type,
            text = self.text)

class PhonyToken(Token):
    def __init__(self, type, position):
        Token.__init__(self, type, '_phony_', position)

###########################################################
# Scanner
###########################################################
class Scanner:
    def __init__(self, charStream):
        self.charStream = charStream # source code
        self.nextToken()

    def error(self):
        raise Exception('{position} : Invalid character \'{char}\'!'.format(
            position = self.charStream.position,
            char = self.charStream.currentChar))

    def nextToken(self):
        '''
        Consume the current token and return the next token.
        '''
        charStream = self.charStream
        charStream.skipWhiteSpace()
        position = charStream.position

        if charStream.currentChar is None:
            self.currentToken = Token(EOF, None, position)
        elif charStream.currentChar.isdigit():
            self.currentToken = self.digits()
        elif charStream.currentChar.isalpha():
            self.currentToken = self.word()
        elif charStream.currentChar == '+':
            self.currentToken = Token(PLUS, '+', position)
            self.charStream.nextChar()
        elif charStream.currentChar == '-':
            self.currentToken = Token(MINUS, '-', position)
            self.charStream.nextChar()
        elif charStream.currentChar == '*':
            self.currentToken = Token(MUL, '*', position)
            self.charStream.nextChar()
        elif charStream.currentChar == '/':
            self.currentToken = Token(DIV, '/', position)
            self.charStream.nextChar()
        elif charStream.currentChar == '(':
            self.currentToken = Token(LPAREN, '(', position)
            self.charStream.nextChar()
        elif charStream.currentChar == ')':
            self.currentToken = Token(RPAREN, ')', position)
            self.charStream.nextChar()
        elif charStream.currentChar == '=':
            self.currentToken = Token(ASSIGN, '=', position)
            self.charStream.nextChar()
        elif charStream.currentChar == ',':
            self.currentToken = Token(COMMA, ',', position)
            self.charStream.nextChar()
        else:
            self.error()

    def digits(self):
        '''
        Extract a unsigned integer token from the source.
        integer ::= ('0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9')+
        '''
        position = self.charStream.position
        text = ''
        while(self.charStream.currentChar is not None and
        self.charStream.currentChar.isdigit()):
            text += self.charStream.currentChar
            self.charStream.nextChar()
        return Token(INTEGER, text, position)

    def word(self):
        '''
        Extract word tokens (identifiers and reserved words).
        identifier ::= letter (letter | digit) *
        '''
        position = self.charStream.position
        text = ''
        while(self.charStream.currentChar is not None and
        (self.charStream.currentChar.isdigit() or
        self.charStream.currentChar.isalpha())):
            text += self.charStream.currentChar
            self.charStream.nextChar()
        if text == 'function':
            return Token(FUNCTION, text, position)
        elif text == 'end':
            return Token(END, text, position)
        elif text == 'return':
            return Token(RETURN, text, position)
        else:
            return Token(IDENTIFIER, text, position)

###########################################################
# Parser
###########################################################
from ast import *
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner

    def error(self):
        text = self.scanner.currentToken.text
        raise Exception('{position} : Syntax error around \'{text}\'!'.format(
            position = self.scanner.currentToken.position,
            text = text if text else 'EOF'))

    def match(self, type):
        '''
        Compare the current token type with the passed token type and if they
        match then consume the current token otherwise raise an exception.
        '''
        token = self.scanner.currentToken
        if token.type == type:
            self.scanner.nextToken()
            return token
        else:
            self.error()

    def arguments(self):
        '''
        Recursive-descent parsing procedure for arguments:
        arguments ::= (expression(',' expression)*)?
        '''
        root = FunctionArgumentsNode(PhonyToken(ARGUMENTS, 0))
        while (self.scanner.currentToken is not None and
        self.scanner.currentToken.type is not RPAREN):
            root.addChild(self.expression())
            if self.scanner.currentToken.type == COMMA:
                self.scanner.nextToken()
        return root

    def parameters(self):
        '''
        Recursive-descent parsing procedure for parameters:
        parameters ::= (identifier(',' identifier)*) ?
        '''
        root = FunctionParametersNode(PhonyToken(PARAMETERS, 0))
        while (self.scanner.currentToken is not None and
        self.scanner.currentToken.type is not RPAREN):
            root.addChild(IdentifierNode(self.match(IDENTIFIER)))
            if self.scanner.currentToken.type == COMMA:
                self.scanner.nextToken()
        return root

    def definition(self):
        '''
        Recursive-descent parsing procedure for function:
        definition ::= '(' parameters ')' statements 'end'
        '''
        root = FunctionDefinitionNode(PhonyToken(DEFINE, 0))
        self.match(LPAREN)
        root.addChild(self.parameters())
        self.match(RPAREN)
        root.addChild(self.statements())
        self.match(END)
        return root

    def prefixexp(self):
        '''
        Recursive-descent parsing procedure for prefixexp:
        prefixexp ::= (identifier | '(' expression ')') ('(' arguments ')')*
        '''
        root = None
        if self.scanner.currentToken.type == IDENTIFIER:
            root = IdentifierNode(self.match(IDENTIFIER))
        elif self.scanner.currentToken.type == LPAREN:
            self.match(LPAREN)
            root = self.expression()
            self.match(RPAREN)

        while (self.scanner.currentToken is not None and
        self.scanner.currentToken.type == LPAREN):
            prefix = root
            root = FunctionCallNode(PhonyToken(CALL, 0))
            root.addChild(prefix)
            self.match(LPAREN)
            root.addChild(self.arguments())
            self.match(RPAREN)

        return root

    def factor(self):
        '''
        Recursive-descent parsing procedure for factor:
        factor ::= integer | ('+'|'-') factor | prefixexp
        '''
        token = self.scanner.currentToken
        if token.type in (PLUS, MINUS):
            self.scanner.nextToken()
            root = UnaryExpressionNode(token)
            root.addChild(self.factor())
            return root
        elif token.type == INTEGER:
            self.match(INTEGER)
            return IntegerNode(token)
        elif token.type in (IDENTIFIER, LPAREN):
            return self.prefixexp()
        else:
            self.error()

    def term(self):
        '''
        Recursive-descent parsing procedure for term:
        term ::= factor (('*'|'/') factor)*
        '''
        root = self.factor()

        while self.scanner.currentToken.type in (MUL, DIV):
            token = self.scanner.currentToken
            self.scanner.nextToken()
            lhs = root
            rhs = self.factor()
            root = BinaryExpressionNode(token)
            root.addChild(lhs)
            root.addChild(rhs)

        return root

    def expression(self):
        '''
        Recursive-descent parsing procedure for expression:
        expression ::= term (('+'|'-') term)* | function
        '''
        if self.scanner.currentToken.type == FUNCTION:
            self.match(FUNCTION)
            return self.definition()
        else:
            root = self.term()

            while self.scanner.currentToken.type in (PLUS, MINUS):
                token = self.scanner.currentToken
                self.scanner.nextToken()
                lhs = root
                rhs = self.term()
                root = BinaryExpressionNode(token)
                root.addChild(lhs)
                root.addChild(rhs)

            return root

    def assignment(self):
        '''
        Recursive-descent parsing procedure for assignment:
        assignment ::= identifier '=' expression | 'function' identifier definition
        '''

	root = None

        if self.scanner.currentToken.type == FUNCTION:
            self.match(FUNCTION)
            target = self.match(IDENTIFIER)
            # phony assign token
            token = Token(ASSIGN, '=', self.scanner.charStream.position)
            root = BinaryExpressionNode(token)
            root.addChild(IdentifierNode(target))
            root.addChild(self.definition())
        else:
            target = self.match(IDENTIFIER)
            root = BinaryExpressionNode(self.match(ASSIGN))
            root.addChild(IdentifierNode(target))
            root.addChild(self.expression())

        return root

    def returnstmt(self):
        '''
        Recursive-descent parsing procedure for returnstmt:
        returnstmt ::= 'return' expression
        '''
        token = self.match(RETURN)
        root = ReturnStatementNode(token)
        root.addChild(self.expression())
        return root

    def statements(self):
        '''
        Recursive-descent parsing procedure for statements:
        statements ::= assignment * returnstmt ?
        '''
        root = StatementListNode(PhonyToken(STATEMENTS, 0))

        while (self.scanner.currentToken is not None and
        self.scanner.currentToken.type == IDENTIFIER or 
        self.scanner.currentToken.type == FUNCTION):
            root.addChild(self.assignment())

        if (self.scanner.currentToken is not None and
        self.scanner.currentToken.type == RETURN):
            root.addChild(self.returnstmt())

        return root

###########################################################
# Top-level script tests
###########################################################
import sys
if __name__ == '__main__':
    while True:
        try:
            if sys.version_info >= (3, 0):
                text = input('calc> ')
            elif sys.version_info >= (2, 0):
                text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue

        scanner = Scanner(CharStream(text))
        parser = Parser(scanner)
        root = parser.statements()
        visitor = PrintVisitor()
        root.accept(visitor)
