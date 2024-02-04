
# Classe genérica para contexto
from nodes import Fun, Var, Assign, Return, Number, Sub, Sum, Mult, Div, Identifier, Param, Block, FunCall, Argument
from memory import RA, Variable

class Context():

    def __init__(self, ast):
        pass

    # encontra e retorna o primeiro nodo de instrução de uma função
    def first(self, node, name):
        funNode = self.getFunNode(node, name)
        return funNode.snd
    
    # encontra e retorna o nodo de definição de uma função
    def getFunNode(self, node, name):
        if node is None:
            raise Exception('funçao nao encontrada: ' + name)
        elif isinstance(node, Fun):
            if node.id.toString() == name: return node
        return self.getFunNode(node.next, name)
    
    # inicializa a memória com as variáveis globais
    def initMemory(self, node):
        if node is None: return
        if isinstance(node, Var):
            self.eval(node)
        self.initMemory(node.next)

    # verifica se um nodo possui chamada de função e retorna a chamada
    def hasFunCall(self, node):
        if isinstance(node, FunCall) and node.rValue is None:
            return node
        
        elif isinstance(node, Var):
            r = self.hasFunCall(node.snd)
            if r is not None:
                return r
            
        elif isinstance(node, Assign):
            r = self.hasFunCall(node.snd)
            if r is not None:
                return r
            
        elif isinstance(node, Return):
            r = self.hasFunCall(node.fst)
            if r is not None:
                return r
            
        elif isinstance(node, Sub) or isinstance(node, Sum) or isinstance(node, Mult) or isinstance(node, Div):
            r = self.hasFunCall(node.fst)
            if r is not None:
                return r
            
            r = self.hasFunCall(node.snd)
            if r is not None:
                return r
            
        return None

    # avalia o nodo atual e pula para o próximo
    def next(self):
        if self.eval(self.current):
            self.current = self.current.next

    def printLine(self):
        print("\nLinha atual: \n > " + self.current.toLineString())

    def printMemory(self):
        print("Estado da memória: ")
        print("<====================>")
        i = len(self.memory) - 1
        for ra in reversed(self.memory):
            print("pos=[" + str(i) + "]")
            print("staticLevel=" + str(ra.staticLevel))
            for var in ra.list:
                print(var.name + ": " + str(var.value))
            print("<====================>")
            i -= 1

    # verifica se chegou ao final do programa
    def end(self):
        return isinstance(self.current, Return) and len(self.binding) == 0
