from rply import ParserGenerator
from nodes import Fun, Var, Assign, Return, Number, Sub, Sum, Mult, Div, Identifier, Param, Block, FunCall, Argument
import lexer
import pydot

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            [lexer.TK_VAR, lexer.TK_OPEN_P, lexer.TK_CLOSE_P, lexer.TK_PLUS,
             lexer.TK_MINUS, lexer.TK_MULT, lexer.TK_DIV, lexer.TK_ASSIGN,
             lexer.TK_FUN, lexer.TK_RETURN, lexer.TK_END, lexer.TK_ID, lexer.TK_COMMA,
             lexer.TK_NUMBER, lexer.TK_OPEN_BR, lexer.TK_CLOSE_BR],
        precedence = [
                ('left', [lexer.TK_PLUS, lexer.TK_MINUS]),
                ('left', [lexer.TK_MULT, lexer.TK_DIV])
                ]
        )
        self.graph = pydot.Dot("ast", graph_type="graph", bgcolor="white")
        self.id = 0

    def parse(self):

        # COMANDOS GLOBAIS
        @self.pg.production('lst_global : var TK_END lst_global')
        @self.pg.production('lst_global : fun TK_END lst_global')
        def lst_global(p): 
            p[0].addNext(p[2])
            return p[0]
        @self.pg.production('lst_global : ')
        def lst_global_end(p):
            return None

        # FUNCAO
        @self.pg.production('fun : TK_FUN TK_ID TK_OPEN_P lst_params TK_CLOSE_P block_fun')
        def fun(p):
            id = Identifier(p[1].value)
            params = p[3]
            body = p[5]
            return Fun(id, params, body)
        
        # LISTA PARAMETROS
        @self.pg.production('lst_params : TK_ID TK_COMMA lst_params')
        def lst_param(p):
            param = Param(p[0].value)
            param.addNext(p[2])
            return param
        @self.pg.production('lst_params : TK_ID')
        def param(p):
            return Param(p[0].value)

        # BLOCO FUNCAO (termina em return)
        @self.pg.production('block_fun : TK_OPEN_BR lst_fun TK_CLOSE_BR')
        def block_fun(p):
            return p[1]
        
        # COMANDOS FUNCAO (termina em return)
        @self.pg.production('lst_fun : var TK_END lst_fun')
        @self.pg.production('lst_fun : assign TK_END lst_fun')
        @self.pg.production('lst_fun : block TK_END lst_fun')
        def lst_fun(p): 
            p[0].addNext(p[2])
            return p[0]
        @self.pg.production('lst_fun : return TK_END')
        def return_fun(p): 
            return p[0]
        
        # BLOCO FUNCAO
        @self.pg.production('block : TK_OPEN_BR lst_block TK_CLOSE_BR')
        def block(p):
            return Block(p[1])
        
        # LISTA BLOCO
        @self.pg.production('lst_block : var TK_END lst_block')
        @self.pg.production('lst_block : assign TK_END lst_block')
        def lst_block(p):
            p[0].addNext(p[2])
            return p[0]
        @self.pg.production('lst_block : ')
        def lst_block_last(p):
            return None
        
        # VAR
        @self.pg.production('var : TK_VAR TK_ID TK_ASSIGN operation')
        def var(p):
            id = Identifier(p[1].value)
            operation = p[3]
            return Var(id, operation)

        # ATRIBUICAO
        @self.pg.production('assign : TK_ID TK_ASSIGN operation')
        def assign(p):
            id = Identifier(p[0].value)
            operation = p[2]
            return Assign(id, operation)

        # RETURN
        @self.pg.production('return : TK_RETURN operation')
        def return_(p):
            operation = p[1]
            return Return(operation)
            
        # OPERAÇÃO
        @self.pg.production('operation : operation TK_PLUS operation')
        @self.pg.production('operation : operation TK_MINUS operation')
        @self.pg.production('operation : operation TK_MULT operation')
        @self.pg.production('operation : operation TK_DIV operation')
        def operation(p):
            fst = p[0]
            snd = p[2]
            operator = p[1]
            if operator.gettokentype() == lexer.TK_PLUS:
                return Sum(fst, snd)
            elif operator.gettokentype() == lexer.TK_MINUS:
                return Sub(fst, snd)
            elif operator.gettokentype() == lexer.TK_MULT:
                return Mult(fst, snd)
            elif operator.gettokentype() == lexer.TK_DIV:
                return Div(fst, snd)

        # NUMERO
        @self.pg.production('operation : TK_NUMBER')
        def number(p):
            return Number(p[0].value)
        
        # IDENTIFICADOR
        @self.pg.production('operation : TK_ID')
        def id(p):
            return Identifier(p[0].value)

        # CHAMADA DE FUNCAO
        @self.pg.production('operation : TK_ID TK_OPEN_P lst_arg TK_CLOSE_P')
        def fun_call(p):
            return FunCall(p[0].value, p[2])
        
        # LISTA ARGUMENTOS
        @self.pg.production('lst_arg : TK_ID TK_COMMA lst_arg')
        def lst_param(p):
            param = Argument(p[0].value)
            param.addNext(p[2])
            return param
        @self.pg.production('lst_arg : TK_ID')
        def param(p):
            return Argument(p[0].value)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()

    def build_graph(self, node):
        self.id += 1
        this_id = self.id

        # BLOCO
        if isinstance(node, Block):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_fst = self.build_graph(node.fst)
            self.graph.add_edge(pydot.Edge(this_id, id_fst, color="black"))
            if node.next is not None:
                id_next = self.build_graph(node.next)
                self.graph.add_edge(pydot.Edge(this_id, id_next, color="black"))

        # FUNCAO
        elif isinstance(node, Fun):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_fst = self.build_graph(node.fst)
            id_snd = self.build_graph(node.snd)
            self.graph.add_edge(pydot.Edge(this_id, id_fst, color="black"))
            self.graph.add_edge(pydot.Edge(this_id, id_snd, color="black"))
            if node.next is not None:
                id_next = self.build_graph(node.next)
                self.graph.add_edge(pydot.Edge(this_id, id_next, color="black"))

        # PARAMETRO / ARGUMENTO
        elif isinstance(node, Param) or isinstance(node, Argument):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            if node.next is not None:
                id_next = self.build_graph(node.next)
                self.graph.add_edge(pydot.Edge(this_id, id_next, color="black"))

        # ATRIBUICAO / VAR
        elif isinstance(node, Assign) or isinstance(node, Var):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_fst = self.build_graph(node.fst)
            id_snd = self.build_graph(node.snd)
            self.graph.add_edge(pydot.Edge(this_id, id_fst, color="black"))
            self.graph.add_edge(pydot.Edge(this_id, id_snd, color="black"))
            if node.next is not None:
                id_next = self.build_graph(node.next)
                self.graph.add_edge(pydot.Edge(this_id, id_next, color="black"))

        # RETURN
        elif isinstance(node, Return):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_fst = self.build_graph(node.fst)
            self.graph.add_edge(pydot.Edge(this_id, id_fst, color="black"))

        # OPERAÇÂO
        elif isinstance(node, Sum) or isinstance(node, Sub) or isinstance(node, Div) or isinstance(node, Mult):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_left = self.build_graph(node.fst)
            id_right = self.build_graph(node.snd)
            self.graph.add_edge(pydot.Edge(this_id, id_left, color="black"))
            self.graph.add_edge(pydot.Edge(this_id, id_right, color="black"))
       
        # NUMERO / IDENTIFICADOR
        elif isinstance(node, Number) or isinstance(node, Identifier):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))

        # CHAMADA DE FUNCAO
        elif isinstance(node, FunCall):
            self.graph.add_node(pydot.Node(this_id, label=node.toString()))
            id_fst = self.build_graph(node.fst)
            self.graph.add_edge(pydot.Edge(this_id, id_fst, color="black"))
        
        return this_id

