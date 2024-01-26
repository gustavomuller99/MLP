from lexer import Lexer
from syntax import Parser
from dynamic import Dynamic
from static import Static
import os
import argparse

test = """
var c = 0;
var b = 0;

fun testA(x) {
  {
    c = 1;
  };
  return 3;
};

fun testB(y) {
  b = 4;
  return 4;
};

fun main(a) {
  var b = 5;
  {
    c = 10;
    b = 2;
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

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help = "0 - estático / 1 - dinâmico")
args = parser.parse_args()

context = Static(ast)
if args.mode == "1":
  context = Dynamic(ast)

while True:
  key = input()
  if key == "":
    os.system('clear')
    context.printMemory()
    context.printLine()

    if context.end() == True: break
    context.next()
