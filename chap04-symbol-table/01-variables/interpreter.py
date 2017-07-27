###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     statements ::= assignment +
#     assignment ::= identifier '=' expression
#     expression ::= term (('+'|'-') term)*
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer | ('+'|'-') factor | '(' expression ')' | identifier
#     ( or factor ::= ('+'|'-')* (integer |'(' expression ')') )
#     integer ::= digit +
#     identifier ::= letter (letter | digit) *
###########################################################

from ast import *
from parser import *
from symbol import *
###########################################################
# Interpreter
# Note that we should return results in both method 'visit'
# in visitors and method 'accept' in ASTs.
###########################################################
class Interpreter(AbstractNodeVisitor):
    def __init__(self):
        self.symval = {}      # variable values
        self.symtab = Scope() # global variables

    def visitBinaryExpressionNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.children[0]) + self.visit(node.children[1])
        elif node.token.type == MINUS:
            return self.visit(node.children[0]) - self.visit(node.children[1])
        elif node.token.type == MUL:
            return self.visit(node.children[0]) * self.visit(node.children[1])
        elif node.token.type == DIV:
            return self.visit(node.children[0]) / self.visit(node.children[1])
        elif node.token.type == ASSIGN:
            name = node.children[0].token.text
            value = self.visit(node.children[1])
            sym = self.symtab.resolve(name)
            if sym is None:
                self.symtab.define(name)
            self.symval[name] = value

    def visitIntegerNode(self, node):
        return int(node.token.text)

    def visitUnaryExpressionNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.children[0])
        elif node.token.type == MINUS:
            return -self.visit(node.children[0])

    def visitIdentifierNode(self, node):
        name = node.token.text
        sym = self.symtab.resolve(name)
        if sym is None:
            raise Exception('{position}: Undefined symbol \'{name}\'!'.format(
                position = node.token.position,
                name = name))
        return self.symval[name]

    def visitStatementListNode(self, node):
        for child in node.children:
            self.visit(child)

###########################################################
# Top-level script tests
###########################################################
import sys, traceback
if __name__ == '__main__':
    interpreter = Interpreter()
    while True:
        try:
            if sys.version_info >= (3, 0):
                text = input('calc> ')
            elif sys.version_info >= (2, 0):
                text = raw_input('calc> ')

            scanner = Scanner(CharStream(text))
            parser = Parser(scanner)
            root = parser.statements()
            root.accept(interpreter)
            print(interpreter.symval)
        except EOFError:
            break
        except Exception:
            traceback.print_exc()
            continue
        if not text:
            continue
