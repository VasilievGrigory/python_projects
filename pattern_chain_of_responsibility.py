import pdb
'''
https://www.coursera.org/learn/oop-patterns-python/programming/B6UXU/riealizovat-chain-of-responsibility
'''

class SomeObject:
    def __init__(self):
        self.integer_field =99
        self.float_field = -4.7797
        self.string_field = "FSDaPR"


class EventGet:
    def __init__(self, variable_type):
        self.variable_type = variable_type
        self.variable = None


class EventSet:
    def __init__(self, variable):
        self.variable_type = type(variable)
        self.variable = variable


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor is not None:
            return self.__successor.handle(char, event)


class StrHandler(NullHandler):

    def handle(self, char, event):
        if event.variable_type == str and event.variable != None:
            char.string_field = event.variable
        elif event.variable_type == str:
            return char.string_field
        else:
            return super().handle(char, event)


class FloatHandler(NullHandler):

    def handle(self, char, event):
        if event.variable_type == float and event.variable != None:
            char.float_field = event.variable
        elif event.variable_type == float:
            print(char.float_field)
            return char.float_field
        else:
            return super().handle(char, event)


class IntHandler(NullHandler):
    def handle(self, char, event):
        if event.variable_type == int and event.variable != None:
            char.integer_field = event.variable
        elif event.variable_type == int:
            return char.integer_field
        else:
            return super().handle(char, event)

if __name__ =="__main__":
    s = SomeObject()
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(s, EventGet(float)))