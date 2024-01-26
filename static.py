# Classe que mantém contexto estático do programa
from nodes import Fun, Var, Assign, Return, Number, Sub, Sum, Mult, Div, Identifier, Param, Block, FunCall, Argument
from memory import RA, Variable
from context import Context

class Static(Context):
    def __init__(self, ast):
        self.root = ast

        self.current = self.first(self.root, "main")
        if (self.current is None): raise Exception("main não encontrada")

        self.memory = []

        globalRA = RA()
        globalRA.staticLevel = 0
        self.memory.append(globalRA)
        self.initMemory(self.root)
        
        mainRA = RA()
        mainRA.staticLevel = 1
        self.memory.append(mainRA)

        self.findStaticLevel(self.root, 0)
        self.currentLevel = 1
        self.raLoadParams = None

        # mantem o ponto de retorno
        self.binding = []
        # mantem o ponto onte o retorno deve ser salvo
        self.bindingR = []
        # mantem o level estático anterior a chamada
        self.bindingLevel = []

    def findStaticLevel(self, node, level):
        if node is None:
            return
        
        elif isinstance(node, Fun):
            node.staticLevel = level + 1
            self.findStaticLevel(node.snd, level + 1)

        elif isinstance(node, Block):
            node.staticLevel = level + 1
            self.findStaticLevel(node.fst, level + 1)

        if isinstance(node, Return) == False:
            self.findStaticLevel(node.next, level)

    # avalia um instrução
    def eval(self, node):
        
        # se houver chamada de funcao, pega o nodo da chamada
        # adiciona o ponto de retorno (self.current) e o ponto onde o retorno da chamada deve ser salvado (funcall)
        # adiciona novo registro de ativação
        # carrega os parametros no novo RA
        funCall = self.hasFunCall(node)
        if funCall is not None:
            fun = self.getFunNode(self.root, funCall.name)

            self.binding.append(self.current)
            self.bindingR.append(funCall)
            self.bindingLevel.append(self.currentLevel)

            self.current = self.first(self.root, funCall.name)
            self.currentLevel = fun.staticLevel

            ra = RA()
            ra.staticLevel = fun.staticLevel
            self.raLoadParams = ra
            self.loadParams(funCall.fst, fun.fst)
            self.memory.append(ra)

            return False
        
        elif isinstance(node, Var):
            name = node.fst.name
            value = self.evalOperation(node.snd)
            self.memory[-1].addVariable(Variable(name, value))

            # é final de um bloco, unico caso em que ocorre
            if node.next is None:
                self.current = self.binding[-1]
                self.currentLevel = self.bindingLevel[-1]

                self.binding.pop()
                self.bindingLevel.pop()
                self.memory.pop()
                
                return False
        
        elif isinstance(node, Assign):
            name = node.fst.name
            value = self.evalOperation(node.snd)
            self.updateVariable(name, value, self.currentLevel)

            # é final de um bloco, unico caso em que ocorre
            if node.next is None:
                self.current = self.binding[-1]
                self.currentLevel = self.bindingLevel[-1]

                self.binding.pop()
                self.bindingLevel.pop()
                self.memory.pop()

                return False

        elif isinstance(node, Block):
            self.binding.append(node.next)
            self.bindingLevel.append(self.currentLevel)

            ra = RA()
            ra.staticLevel = self.currentLevel + 1
            self.memory.append(ra)

            self.current = node.fst
            self.currentLevel = self.currentLevel + 1

            return False
        
        # se for retorno, retorno para ponto anterior a chamada
        # salva retorno da função
        # pop nas estruturas necessarias
        elif isinstance(node, Return):
            self.current = self.binding[-1]
            self.currentLevel = self.bindingLevel[-1]
            self.bindingR[-1].rValue = self.evalOperation(node.fst)

            self.binding.pop()
            self.bindingR.pop()
            self.bindingLevel.pop()
            self.memory.pop()

            return False
        
        return True
    
    # carrega parametros da chamada de funcao
    def loadParams(self, call, fun):
        if call is None and fun is None:
            return
        if call is None or fun is None:
            raise Exception('argumentos não batem com definição')
        self.raLoadParams.addVariable(Variable(fun.name, self.getVariable(call.name, self.currentLevel).value))
        self.loadParams(call.next, fun.next)

    # avalia uma operacao para um valor NUMERICO, apos as chamadas terem sido avaliadas
    def evalOperation(self, node):
        if isinstance(node, Sum):
            return self.evalOperation(node.fst) + self.evalOperation(node.snd)
        
        elif isinstance(node, Mult):
            return self.evalOperation(node.fst) * self.evalOperation(node.snd)
        
        elif isinstance(node, Div):
            return self.evalOperation(node.fst) / self.evalOperation(node.snd)
        
        elif isinstance(node, Sub):
            return self.evalOperation(node.fst) - self.evalOperation(node.snd)
        
        elif isinstance(node, Number):
            return int(node.value)
        
        elif isinstance(node, Identifier):
            return self.getVariable(node.name, self.currentLevel).value
        
        elif isinstance(node, FunCall):
            return node.rValue

    def updateVariable(self, name, value, level):
        for ra in reversed(self.memory):
            if ra.staticLevel == level:
                level -= 1
                if ra.updateVariable(name, value):
                    return
        raise Exception('variavel não encontrada: ' + name)

    def getVariable(self, name, level):
        for ra in reversed(self.memory):
            if ra.staticLevel == level:
                level -= 1
                var = ra.getVariable(name)
                if var is not None: 
                    return var
        raise Exception('variavel não encontrada: ' + name)
