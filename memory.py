# Classes que definem o registro de ativação

class RA:
    def __init__(self):
        self.list = []

    def addVariable(self, var):
        if len(list(filter(lambda x: x.name == var.name, self.list))) != 0: 
            raise Exception("variável redeclarada")
        self.list.append(var)

    def getVariable(self, name):
        var = list(filter(lambda x: x.name == name, self.list))
        if len(var) != 0: 
            return var[0]
        else: 
            return None

    def updateVariable(self, name, value):
        index = list([(idx, var) for idx, var in enumerate(self.list) if var.name == name])
        if len(index) != 0:
            self.list[index[0][0]].value = value
            return True
        else:
            return False

    
class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
