###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     expr ::= term (('+'|'-') term)*
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer | ('+'|'-') factor | '(' expr ')'
#     ( or factor ::= ('+'|'-')* (integer |'(' expr ')') )
#     integer ::= ('0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9')+
###########################################################

from ast import *
from parser import *
###########################################################
# Interpreter
# Note that we should return results in both method 'visit'
# in visitors and method 'accept' in ASTs.
###########################################################
class Interpreter(AbstractNodeVisitor):
    def visitBinaryExprNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.children[0]) + self.visit(node.children[1])
        elif node.token.type == MINUS:
            return self.visit(node.children[0]) - self.visit(node.children[1])
        elif node.token.type == MUL:
            return self.visit(node.children[0]) * self.visit(node.children[1])
        elif node.token.type == DIV:
            return self.visit(node.children[0]) / self.visit(node.children[1])

    def visitIntegerNode(self, node):
        return int(node.token.text)

    def visitUnaryExprNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.children[0])
        elif node.token.type == MINUS:
            return -self.visit(node.children[0])

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
            scanner = Scanner(TextStream(text))
            parser = Parser(scanner)
            root = parser.expr()
            interpreter = Interpreter()
            print(root.accept(interpreter))
        except Exception as e:
            print(e)
