# Classe que mantém contexto dinâmico do programa
from nodes import Fun, Var, Assign, Return, Number, Sub, Sum, Mult, Div, Identifier, Param, Block, FunCall, Argument
from memory import RA, Variable
from context import Context

class Dynamic(Context):
    
    # inicializa contexto:
    # procura primeiro nodo da MAIN
    # adiciona RA global e avalia variaveis globais
    # adiciona RA da main
    def __init__(self, ast):
        self.root = ast

        self.current = self.first(self.root, "main")
        if (self.current is None): raise Exception("main não encontrada")

        self.memory = []
        self.memory.append(RA())
        self.initMemory(self.root)
        self.memory.append(RA())

        self.binding = []
        self.bindingR = []
    
    # avalia um instrução
    def eval(self, node):
        
        # se houver chamada de funcao, pega o nodo da chamada
        # adiciona o ponto de retorno (self.current) e o ponto onde o retorno da chamada deve ser salvado (funcall)
        # adiciona novo registro de ativação
        # carrega os parametros no novo RA
        funCall = self.hasFunCall(node)
        if funCall is not None:
            self.binding.append(self.current)
            self.bindingR.append(funCall)
            self.current = self.first(self.root, funCall.name)
            self.memory.append(RA())
            self.loadParams(funCall.fst, self.getFunNode(self.root, funCall.name).fst)
            return False
        
        elif isinstance(node, Var):
            name = node.fst.name
            value = self.evalOperation(node.snd)
            self.memory[-1].addVariable(Variable(name, value))

            # é final de um bloco, unico caso em que ocorre
            if node.next is None:
                self.current = self.binding[-1]
                self.binding.pop()
                self.memory.pop()
                return False
        
        elif isinstance(node, Assign):
            name = node.fst.name
            value = self.evalOperation(node.snd)
            self.updateVariable(name, value)

            # é final de um bloco, unico caso em que ocorre
            if node.next is None:
                self.current = self.binding[-1]
                self.binding.pop()
                self.memory.pop()
                return False

        elif isinstance(node, Block):
            self.binding.append(node.next)
            self.memory.append(RA())
            self.current = node.fst
            return False
        
        # se for retorno, retorno para ponto anterior a chamada
        # salva retorno da função
        # pop nas estruturas necessarias
        elif isinstance(node, Return):
            self.current = self.binding[-1]
            self.bindingR[-1].rValue = self.evalOperation(node.fst)
            self.binding.pop()
            self.bindingR.pop()
            self.memory.pop()
            return False
        
        return True
    
    # carrega parametros da chamada de funcao
    def loadParams(self, call, fun):
        if call is None and fun is None:
            return
        if call is None or fun is None:
            raise Exception('argumentos não batem com definição')
        self.memory[-1].addVariable(Variable(fun.name, self.getVariable(call.name).value))
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
            return self.getVariable(node.name).value
        
        elif isinstance(node, FunCall):
            return node.rValue

    # atualiza o valor de uma variavel    
    def updateVariable(self, name, value):
        for ra in reversed(self.memory):
            if ra.updateVariable(name, value):
                return
        raise Exception('variavel não encontrada: ' + name)

    # retorna uma variavel
    def getVariable(self, name):
        for ra in reversed(self.memory):
            var = ra.getVariable(name)
            if var is not None: 
                return var
        raise Exception('variavel não encontrada: ' + name)
        