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
        if isinstance(node, BinaryExpressionNode):
            return self.visitBinaryExpressionNode(node)
        elif isinstance(node, IntegerNode):
            return self.visitIntegerNode(node)
        elif isinstance(node, UnaryExpressionNode):
            return self.visitUnaryExpressionNode(node)
        elif isinstance(node, IdentifierNode):
            return self.visitIdentifierNode(node)
        elif isinstance(node, StatementListNode):
            return self.visitStatementListNode(node)
        elif isinstance(node, FunctionArgumentsNode):
            return self.visitFunctionArgumentsNode(node)
        elif isinstance(node, FunctionParametersNode):
            return self.visitFunctionParametersNode(node)
        elif isinstance(node, FunctionDefinitionNode):
            return self.visitFunctionDefinitionNode(node)
        elif isinstance(node, FunctionCallNode):
            return self.visitFunctionCallNode(node)
        elif isinstance(node, ReturnStatementNode):
            return self.visitReturnStatementNode(node)

    @abstractmethod
    def visitBinaryExpressionNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitIntegerNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitUnaryExpressionNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitIdentifierNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitStatementListNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitFunctionArgumentsNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitFunctionParametersNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitFunctionDefinitionNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitFunctionCallNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitReturnStatementNode(self, node):
        raise NotImplementedError(NOT_IMPLEMENTED)

###########################################################
# BinaryExpressionNode -- AST Node of Expression
###########################################################
class BinaryExpressionNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# IntegerNode -- AST Node of Integer
###########################################################
class IntegerNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# UnaryExpressionNode -- AST Node of Unary Expression
###########################################################
class UnaryExpressionNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# IdentifierNode -- AST Node of Variable
###########################################################
class IdentifierNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# StatementListNode -- AST Node of Statement List
###########################################################
class StatementListNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# FunctionArgumentsNode -- AST Node of arguments
###########################################################
class FunctionArgumentsNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# FunctionParametersNode -- AST Node of parameters
###########################################################
class FunctionParametersNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# FunctionDefinitionNode -- AST Node of function definition
###########################################################
class FunctionDefinitionNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# FunctionCallNode -- AST Node of function call
###########################################################
class FunctionCallNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# ReturnStatementNode -- AST Node of Return Statement
###########################################################
class ReturnStatementNode(AbstractNode):
    def accept(self, visitor):
        return visitor.visit(self)

###########################################################
# PrintVisitor
###########################################################
class PrintVisitor(AbstractNodeVisitor):
    def __init__(self, leadingSpace = 0):
        self.leadingSpace = leadingSpace
        self.indentLevel = 0

    def indent(self):
        self.indentLevel += 1

    def unindent(self):
        self.indentLevel -= 1

    def write(self, content):
        print ' '*(4*self.indentLevel+self.leadingSpace), content

    def visitBinaryExpressionNode(self, node):
        self.write(node.token)
        self.indent()
        for child in node.children:
            child.accept(self)
        self.unindent()

    def visitIntegerNode(self, node):
        self.write(node.token)

    def visitUnaryExpressionNode(self, node):
        self.write('{token} (Unary)'.format(token = node.token))
        self.indent()
        for child in node.children:
            child.accept(self)
        self.unindent()

    def visitIdentifierNode(self, node):
        self.write(node.token)

    def visitStatementListNode(self, node):
        self.write(node.token)
        self.indent()
        for child in node.children:
            child.accept(self)
        self.unindent()

    def visitFunctionArgumentsNode(self, node):
        pass # do nothing here, process it in function call

    def visitFunctionParametersNode(self, node):
        pass # do nothing here, process it in function definition

    def visitFunctionCallNode(self, node):
        self.write('function call (prefix part):')
        self.indent()
        node.children[0].accept(self)
        self.unindent()

        self.write('function call (arguments part):')
        self.indent()
        if len(node.children[1].children) == 0:
			self.write('<null>')
        else:
            for child in node.children[1].children:
                child.accept(self)
        self.unindent()

    def visitFunctionDefinitionNode(self, node):
        self.write('function definition (parameters part):')
        self.indent()
        if len(node.children[0].children) == 0:
			self.write('<null>')
        else:
            for child in node.children[0].children:
                child.accept(self)
        self.unindent()

        self.write('function definition (body part):')
        self.indent()
        node.children[1].accept(self)
        self.unindent()

    def visitReturnStatementNode(self, node):
        self.write(node.token)
        self.indent()
        for child in node.children:
            child.accept(self)
        self.unindent()

###########################################################
# Top-level script tests
###########################################################
if __name__ == '__main__':
    # AST of '3 * 2 + 5'
    operand1 = IntegerNode('3')
    operand2 = IntegerNode('2')
    operand3 = IntegerNode('5')

    mult = BinaryExpressionNode('*')
    root = BinaryExpressionNode('+')

    mult.addChild(operand1)
    mult.addChild(operand2)

    root.addChild(mult)
    root.addChild(operand3)

    visitor = PrintVisitor();
    root.accept(visitor)
