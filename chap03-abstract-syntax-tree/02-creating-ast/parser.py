###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     expression ::= term (('+'|'-') term)*
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer
#     integer ::= ('0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9')+
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
INTEGER, PLUS, MINUS, MUL, DIV, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'
    )
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
            self.currentToken = Token(INTEGER, self.digits(), position)
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
        else:
            self.error()

    def digits(self):
        '''
        Extract a unsigned integer token from the source.
        integer ::= ('0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9')+
        '''
        result = ''
        while(self.charStream.currentChar is not None and
        self.charStream.currentChar.isdigit()):
            result += self.charStream.currentChar
            self.charStream.nextChar()
        return result

###########################################################
# Parser
###########################################################
from ast import *
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner

    def error(self):
        raise Exception('{position} : Syntax error at \'{text}\'!'.format(
            position = self.scanner.currentToken.position,
            text = self.scanner.currentToken.text))

    def match(self, type):
        '''
        Compare the current token type with the passed token type and if they
        match then consume the current token otherwise raise an exception.
        '''
        if self.scanner.currentToken.type == type:
            self.scanner.nextToken()
            return True
        else:
            self.error()

    def factor(self):
        '''
        Recursive-descent parsing procedure for factor:
        factor ::= integer
        '''
        token = self.scanner.currentToken
        self.match(INTEGER)
        return IntegerNode(token)

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
        expression::= term (('+'|'-') term)*
        '''
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

        try:
            scanner = Scanner(CharStream(text))
            parser = Parser(scanner)
            root = parser.expression()
            visitor = PrintVisitor()
            root.accept(visitor)
        except Exception as e:
            print(e)
