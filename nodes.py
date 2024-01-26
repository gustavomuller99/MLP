# BLOCO
class Block():
    def __init__(self, fst):
        self.fst = fst
        self.next = None
        self.staticLevel = None

    def addNext(self, next):
        self.next = next
    
    def toString(self):
        return "{ }"
    
    def toLineString(self):
        return "{ };"

# FUNCAO
class Fun():
    def __init__(self, id, fst, snd):
        self.id = id
        self.fst = fst
        self.snd = snd
        self.next = None
        self.staticLevel = None

    def addNext(self, next):
        self.next = next
    
    def toString(self):
        return "fun " + self.id.toString()
    
# PARAMETRO
class Param():
    def __init__(self, name):
        self.name = name
        self.next = None

    def addNext(self, next):
        self.next = next
    
    def toString(self):
        return self.name
    
# VARIAVEIS
class Var():
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd
        self.next = None

    def addNext(self, next):
        self.next = next

    def toString(self):
        return "var"
    
    def toLineString(self):
        return "var " + self.fst.toLineString() + " = " + self.snd.toLineString() + ";"

# ATRIBUICAO
class Assign():
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd
        self.next = None

    def addNext(self, next):
        self.next = next

    def toString(self):
        return "="
    
    def toLineString(self):
        return self.fst.toLineString() + " = " + self.snd.toLineString() + ";"

# RETURN
class Return():
    def __init__(self, fst):
        self.fst = fst

    def toString(self):
        return "return"
    
    def toLineString(self):
        return "return " + self.fst.toLineString() + ";"
    
# CHAMADA DE FUNCAO
class FunCall():
    def __init__(self, name, fst):
        self.name = name
        self.fst = fst
        self.rValue = None
    
    def toString(self):
        return self.name + "()"
    
    def toLineString(self):
        return self.name + "(" + self.fst.toLineString() + ")"
    
    def returnValue(self, value):
        self.rValue = value

# ARGUMENTO
class Argument():
    def __init__(self, name):
        self.name = name
        self.next = None

    def addNext(self, next):
        self.next = next
    
    def toString(self):
        return self.name   
    
    def toLineString(self):
        if self.next is None: return self.name
        else: return self.name + ", " + self.next.toLineString()

# IDENTIFICADOR
class Identifier():
    def __init__(self, name):
        self.name = name
    
    def toString(self):
        return self.name
    
    def toLineString(self):
        return self.name
    
# NUMERO
class Number():
    def __init__(self, value):
        self.value = value
    
    def toString(self):
        return str(self.value)
    
    def toLineString(self):
        return str(self.value)

# OPERACOES
class BinaryOp():
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd        


class Sum(BinaryOp):
    def toString(self):
        return "+"
    
    def toLineString(self):
        return self.fst.toLineString() + " + " + self.snd.toLineString()


class Sub(BinaryOp):
    def toString(self):
        return "-"
    
    def toLineString(self):
        return self.fst.toLineString() + " - " + self.snd.toLineString()


class Mult(BinaryOp):
    def toString(self):
        return "*"
    
    def toLineString(self):
        return self.fst.toLineString() + " * " + self.snd.toLineString()

    
class Div(BinaryOp):
    def toString(self):
        return "/"
    
    def toLineString(self):
        return self.fst.toLineString() + " / " + self.snd.toLineString()

    
