import notery.parsing.lexer as lexer
import notery.cmdline.logger as logger

#
# BLOCK
#
# Contains local context
class Block:
    def __init__(self, parent):
        self.lets = []
        self.sets = []
        self.constants = []
        self.functions = []
        self.content = []

    def add(self, x):
        ls = None
        if   isinstance(x, Let): ls = self.lets
        elif isinstance(x, Set): ls = self.sets
        elif isinstance(x, Constant): ls = self.constants
        elif isinstance(x, Function): ls = self.functions
        elif isinstance(x, FunctionInvocation): ls = self.content
        elif isinstance(x, ConstantReference): ls = self.content
        elif isinstance(x, Value): ls = self.content
        ls.append(x)

#
# FUNCTION
#
class Function:
    def __init__(self, name, args, result):
        self.name = name
        self.args = args
        self.result = result

class FunctionArgument:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class FunctionInvocation:
    def __init__(self, name, args):
        self.name = name
        self.args = args

#
# CONSTANT
#
class Constant:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ConstantReference:
    def __init__(self, name):
        self.name = name

class Let:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Set:
    def __init__(self, name, value):
        self.name = name
        self.value = value

#
# VALUE
#
# Both `value`s and `type`s are Values.
# `value`s have a type `type`, and
# `type`s have the type Type.
class Value:
    def __init__(self, value, type):
        self.value = value
        self.type = type

#
# PARSE
#
def parse(lexed):

    block = None

    def parse_functioninvocation(x): pass

    def parse_functionreference(x): pass

    def parse_constantreference(x): pass

    def parse_phrase(x): pass

    def parse_helper(x):
        if isinstance(x, lexer.FunctionInvocation):
            return parse_functioninvocation(x)
        elif isinstance(x, lexer.FunctionReference):
            return parse_functionreference(x)
        elif isinstance(x, lexer.ConstantReference):
            return parse_constantreference(x)
        elif isinstance(x, str):
            print("string:",x)

    for x in lexed: parse_helper(x)