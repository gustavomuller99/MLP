# Classe que mantém contexto estático do programa
from nodes import Fun, Var, Assign, Return, Number, Sub, Sum, Mult, Div, Identifier, Param, Block, FunCall, Argument
from memory import RA, Variable
from context import Context

class Static(Context):
    def __init__():
        pass

    def eval(self, node):
        pass

    def loadParams(self, call, fun):
        pass

    def evalOperation(self, node):
        pass

    def updateVariable(self, name, value):
        pass

    def getVariable(self, name):
        pass
