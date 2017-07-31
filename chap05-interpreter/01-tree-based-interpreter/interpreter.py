###########################################################
# Implementation of an Simple Interpreter
# Syntax:
#     stmtlist ::= assignment * returnstmt ?
#     returnstmt ::= 'return' expr
#     assignment ::= identifier '=' expr
#     expr ::= term (('+'|'-') term)* | function
#     arguments ::= (expr(',' expr)*)?
#     function ::= 'function' '(' parameters ')' stmtlist 'end'
#     parameters ::= (var(',' var)*) ?
#     term ::= factor (('*'|'/') factor)*
#     factor ::= integer | ('+'|'-') factor | prefixexp
#     ( or factor ::= ('+'|'-')* (integer | prefixexp) )
#     prefixexp ::= (identifier | '(' expr ')') ('(' arguments ')')*
#     integer ::= digit +
#     identifier ::= letter (letter | digit) *
###########################################################

from ast import *
from parser import *
from memory import *
###########################################################
# Interpreter
# Note that we should return results in both method 'visit'
# in visitors and method 'accept' in ASTs.
###########################################################
class Interpreter(AbstractNodeVisitor):
    def __init__(self):
        # self.globalScope = Scope() # global scope is filled by the parser
        self.globalSpace = MemorySpace('globals')  # global memory
        self.currentSpace = self.globalSpace
        self.callStack = [] # call stack

    def getSpaceWithSymbol(self, id):
        '''
        Return scope holding id's value; current func space or global.
        '''
        if self.currentSpace.retrieve(id):
            return self.currentSpace
        elif self.globalSpace.retrieve(id):
            return self.globalSpace
        else:
            return None

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
            space = self.getSpaceWithSymbol(name)
            if space is not None:
                space.update(name, value)
            self.currentSpace.enter(name, value)

    def visitIntegerNode(self, node):
        return int(node.token.text)

    def visitUnaryExpressionNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.children[0])
        elif node.token.type == MINUS:
            return -self.visit(node.children[0])

    def visitIdentifierNode(self, node):
        name = node.token.text
        space = self.getSpaceWithSymbol(name)
        if space is None:
            raise Exception('{position} : Undefined symbol \'{name}\'!'.format(
                position = node.token.position,
                name = name))
        return space.retrieve(name)

    def visitStatementListNode(self, node):
        for child in node.children:
            self.visit(child)

    def visitFunctionArgumentsNode(self, node):
        pass # do nothing here, process it in function call

    def visitFunctionParametersNode(self, node):
        pass # do nothing here, process it in function definition

    def visitFunctionCallNode(self, node):
        # For the sake of simplicity, closures are not considered here.

        # function funcprototype, AST node
        funcproto = node.children[0].accept(self)

        # function parameters
        funcpars = funcproto.children[0]
        # function body
        funcbody = funcproto.children[1]

        # function arguments (of call)
        funcargs = node.children[1]

        # check arguments and parameters number
        if len(funcpars.children) != len(funcargs.children):
            raise Exception('{position}: Arguments mismatch!'.format(
                position = node.token.position))

        # create a new memory space for calling function
        funcspace = MemorySpace('{function}'.format(
            function = funcproto.token.text))
        funcspace.enter('ans', None)  # return value

        for i in range(len(funcargs.children)):
            funcspace.enter(funcpars.children[i].token.text,
                            funcargs.children[i].accept(self))

        # call function
        saveSpace = self.currentSpace
        self.callStack.append(funcspace)
        self.currentSpace = funcspace
        funcbody.accept(self)
        ans = funcspace.retrieve('ans')
        self.callStack.pop()
        self.currentSpace = saveSpace
        return ans

    def visitFunctionDefinitionNode(self, node):
        # do nothing here
        return node

    def visitReturnStatementNode(self, node):
        self.currentSpace.enter('ans', node.children[0].accept(self))

###########################################################
# Top-level script tests
###########################################################
import sys, traceback
if __name__ == '__main__':
    '''
    Enter a script, for example:
    f = function(x, y) return x+y end
    a = f(3, 4)
    '''
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
            print(interpreter.globalSpace)
        except EOFError:
            break
        except Exception:
            traceback.print_exc()
            continue
        if not text:
            continue
