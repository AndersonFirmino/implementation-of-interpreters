###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     chunk ::= assignment +
#     assignment ::= var '=' expr
#     expr ::= term (('+'|'-') term)*
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer | ('+'|'-') factor | '(' expr ')' | var
#     ( or factor ::= ('+'|'-')* (integer |'(' expr ')') )
#     integer ::= digit +
#     var ::= letter (letter | digit) *
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
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, VAR, ASSIGN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'VAR', 'ASSIGN', 'EOF',
    )

# Phony token types -- Used in creating AST nodes that don't derived from tokens
# So, we can get node type va token.type
CHUNK = ('CHUNK')

class Token:
    def __init__(self, type, text, position):
        self.type = type         # token type
        self.text = text         # token text
        self.position = position # position of the first token character

    def __str__(self):
        return '{position} : ({type}, {text})'.format(
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
        var ::= letter (letter | digit) *
        '''
        position = self.charStream.position
        text = ''
        while(self.charStream.currentChar is not None and
        (self.charStream.currentChar.isdigit() or
        self.charStream.currentChar.isalpha())):
            text += self.charStream.currentChar
            self.charStream.nextChar()
        return Token(VAR, text, position)

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

    def factor(self):
        '''
        Recursive-descent parsing procedure for factor:
        factor ::= integer | ('+'|'-') factor | '(' expr ')'
        '''
        token = self.scanner.currentToken
        if token.type in (PLUS, MINUS):
            self.scanner.nextToken()
            root = UnaryExprNode(token)
            root.addChild(self.factor())
            return root
        elif token.type == INTEGER:
            self.match(INTEGER)
            return IntegerNode(token)
        elif token.type == VAR:
            self.match(VAR)
            return VarNode(token)
        elif token.type == LPAREN:
            self.match(LPAREN)
            root = self.expr()
            self.match(RPAREN)
            return root
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
            root = BinaryExprNode(token)
            root.addChild(lhs)
            root.addChild(rhs)

        return root

    def expr(self):
        '''
        Recursive-descent parsing procedure for expr:
        expr ::= term (('+'|'-') term)*
        '''
        root = self.term()

        while self.scanner.currentToken.type in (PLUS, MINUS):
            token = self.scanner.currentToken
            self.scanner.nextToken()
            lhs = root
            rhs = self.term()
            root = BinaryExprNode(token)
            root.addChild(lhs)
            root.addChild(rhs)

        return root

    def assignment(self):
        '''
        Recursive-descent parsing procedure for assignment:
        assignment ::= var '=' expr
        '''
        target = self.match(VAR)
        if target is not None:
            root = BinaryExprNode(self.match(ASSIGN))
            root.addChild(VarNode(target))
            root.addChild(self.expr())
            return root
        else:
            self.error()

    def chunk(self):
        '''
        Recursive-descent parsing procedure for chunk:
        chunk ::= assignment +:
        '''
        root = ChunkNode(PhonyToken(CHUNK, 0))
        root.addChild(self.assignment())

        while(self.scanner.currentToken is not None and
        self.scanner.currentToken.type is not EOF):
            root.addChild(self.assignment())

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
        root = parser.chunk()
        visitor = PrintVisitor()
        root.accept(visitor)
