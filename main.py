from lexer import Lexer
from syntax import Parser
from dynamic import Dynamic
import os

test = """
var c = 0;

fun testA(x) {
  return 3;
};

fun testB(y) {
  return 4;
};

fun main(a) {
  var b = 5;
  {
    b = 3;
    c = 4; 
    var x = c;
    x = 1;
  };
  c = testA(b) + testB(c);
  return 0;
};
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(test)

pg = Parser()
pg.parse()
parser = pg.get_parser()
ast = parser.parse(tokens)

pg.build_graph(ast)
pg.graph.write_png("ast.png")

context = Dynamic(ast)

while True:
  key = input()
  if key == "":
    os.system('clear')
    context.printMemory()
    context.printLine()

    if context.end() == True: break
    context.next()
