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
    def visit(self, element):
        raise NotImplementedError(NOT_IMPLEMENTED)


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
        for element in self.elements:
            element.accept(visitor)
        visitor.visit(self)


class CarElementDoVisitor(CarElementVisitor):
    element_type = None

    def visit(self, element):
        self.element_type = type(element)

        if self.element_type == Body:
            print("Moving my body.")
        elif self.element_type == Car:
            print("Starting my car.")
        elif self.element_type == Wheel:
            print("Kicking my {} wheel.".format(element.name))
        elif self.element_type == Engine:
            print("Starting my engine.")
        else:
            raise NotImplementedError(
                "Not implemented for type {}.".format(self.element_type)
            )


class CarElementPrintVisitor(CarElementVisitor):
    element_type = None

    def visit(self, element):
        self.element_type = type(element)

        if self.element_type == Body:
            print("Visiting body.")
        elif self.element_type == Car:
            print("Visiting car.")
        elif self.element_type == Wheel:
            print("Visiting {} wheel.".format(element.name))
        elif self.element_type == Engine:
            print("Visiting engine.")
        else:
            raise NotImplementedError(
                "Not implemented for type {}.".format(self.element_type)
            )


car = Car()
car.accept(CarElementPrintVisitor())
car.accept(CarElementDoVisitor())
