"""
Visitor Pattern in Python
https://en.wikipedia.org/wiki/Visitor_pattern
"""

from abc import ABCMeta, abstractmethod

NOT_IMPLEMENTED = "You should implement this."


class CarElement:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, visitor):
        raise NotImplementedError(NOT_IMPLEMENTED)


class CarElementVisitor:
    __metaclass__ = ABCMeta

    @abstractmethod
    def visitBody(self, element):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitEngine(self, element):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitWheel(self, element):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visitCar(self, element):
        raise NotImplementedError(NOT_IMPLEMENTED)

    def visit(self, element):
        if isinstance(element, Body):
            self.visitBody(element)
        elif isinstance(element, Engine):
            self.visitEngine(element)
        elif isinstance(element, Wheel):
            self.visitWheel(element)
        elif isinstance(element, Car):
            self.visitCar(element)


class Body(CarElement):
    def accept(self, visitor):
        visitor.visit(self)


class Engine(CarElement):
    def accept(self, visitor):
        visitor.visit(self)


class Wheel(CarElement):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        visitor.visit(self)

class Car(CarElement):
    def __init__(self):
        self.elements = [
            Wheel("front left"), Wheel("front right"),
            Wheel("back left"), Wheel("back right"),
            Body(), Engine()
        ]

    def accept(self, visitor):
        visitor.visit(self)


class CarElementDoVisitor(CarElementVisitor):
    def visitBody(self, element):
        print("Moving my body.")

    def visitEngine(self, element):
        print("Starting my car.")

    def visitWheel(self, element):
        print("Kicking my {} wheel.".format(element.name))

    def visitCar(self, element):
        for element in element.elements:
            element.accept(self)
        print("Starting my engine.")


class CarElementPrintVisitor(CarElementVisitor):
    def visitBody(self, element):
        print("Visiting my body.")

    def visitEngine(self, element):
        print("Visiting my car.")

    def visitWheel(self, element):
        print("Visiting my {} wheel.".format(element.name))

    def visitCar(self, element):
        for element in element.elements:
            element.accept(self)
        print("Visiting my engine.")


car = Car()
car.accept(CarElementPrintVisitor())
car.accept(CarElementDoVisitor())
