###########################################################
# Abstract Syntax Tree and Visitor Pattern Implementation
###########################################################

from abc import ABCMeta, abstractmethod

NOT_IMPLEMENTED = "Abstract method not implemented."

###########################################################
# AbstractNode -- Abstract Node of AST
###########################################################
class AbstractNode:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError(NOT_IMPLEMENTED)

    def __init__(self, token):
        self.token = token
        self.children = []

    def addChild(self, node):
        self.children.append(node)

###########################################################
# AbstractNodeVisitor -- Abstract Visitor of Node
###########################################################
class AbstractNodeVisitor:
    __metaclass__ = ABCMeta

    def visit(self, node):
        if isinstance(node, BinaryExprNode):
            self.visitBinaryExprNode(node)
        elif isinstance(node, IntegerNode):
            self.visitIntegerNode(node)

    @abstractmethod
    def visitBinaryExprNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitIntegerNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

###########################################################
# BinaryExprNode -- AST Node of Expression
###########################################################
class BinaryExprNode(AbstractNode):
    def accept(self, visitor):
        for node in self.children:
            node.accept(visitor)
        visitor.visit(self)

###########################################################
# IntegerNode -- AST Node of Integer
###########################################################
class IntegerNode(AbstractNode):
    def accept(self, visitor):
        visitor.visit(self)

###########################################################
# PrintVisitor
###########################################################
class PrintVisitor(AbstractNodeVisitor):
    def visitBinaryExprNode(self, node):
        print(node.token)

    def visitIntegerNode(self, node):
        print(node.token)

###########################################################
# Top-level script tests
###########################################################
if __name__ == '__main__':
    # AST of '3 * 2 + 5'
    operand1 = IntegerNode('3')
    operand2 = IntegerNode('2')
    operand3 = IntegerNode('5')

    mult = BinaryExprNode('*')
    root = BinaryExprNode('+')

    mult.addChild(operand1)
    mult.addChild(operand2)

    root.addChild(mult)
    root.addChild(operand3)

    visitor = PrintVisitor();
    root.accept(visitor)
