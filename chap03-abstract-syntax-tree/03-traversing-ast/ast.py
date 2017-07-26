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
            return self.visitBinaryExprNode(node)
        elif isinstance(node, IntegerNode):
            return self.visitIntegerNode(node)
        elif isinstance(node, UnaryExprNode):
            return self.visitUnaryExprNode(node)

    @abstractmethod
    def visitBinaryExprNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitIntegerNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitUnaryExprNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

###########################################################
# BinaryExprNode -- AST Node of Expression
###########################################################
class BinaryExprNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# IntegerNode -- AST Node of Integer
###########################################################
class IntegerNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# UnaryExprNode -- AST Node of Unary Expression
###########################################################
class UnaryExprNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# PrintVisitor
###########################################################
class PrintVisitor(AbstractNodeVisitor):
    def visitBinaryExprNode(self, node):
        for child in node.children:
            child.accept(self)
        print(node.token)

    def visitIntegerNode(self, node):
        print(node.token)

    def visitUnaryExprNode(self, node):
        for child in node.children:
            child.accept(self)
        print('{token} (Unary)'.format(token = node.token))

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
