import notery.cmdline.logger as logger
import notery.parsing.lexer as lexer
from notery.keywords import builtins

#
# INVOCATION
#
class Invocation:

    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.context = Context()

    def tostring(self):
        s = "$(" + self.name + " ("
        for a in self.args:
            s += str(a) + " | "
        if s.endswith(" | "): s = s[:-3]
        s += ") )"
        return s
    __str__ = tostring
    __repr__ = tostring

#
# FUNCTION
#
class Function:

    def __init__(self, name, args, result):
        self.name = name
        self.args = args
        self.result = result

    def tostring(self):
        s = "(function " + str(self.name)
        s += " ("
        for a in self.args: s += str(a)
        s += ") => "
        s += str(self.result)
        s += ")"
        return s
    __str__ = tostring
    __repr__ = tostring

#
# FUNCTION REFERENCE
#
class FunctionReference:

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return "->" + str(self.name)
    __str__ = tostring
    __repr__ = tostring

#
# LET
#
class Let:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def tostring(self):
        return "(" + str(self.name) + " : " + str(self.type) + ")"
    __str__ = tostring
    __repr__ = tostring

#
# CONSTANT
#
class Constant:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def tostring(self):
        return "(" + str(self.name) + " := " + str(self.value) + ")"
    __str__ = tostring
    __repr__ = tostring

#
# CONSTANT REFERENCE
#
class ConstantReference:

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return "$" + str(self.name)
    __str__ = tostring
    __repr__ = tostring

#
# VALUE
#
class Value:

    def __init__(self, value, type):
        self.value = value
        self.type = type

    def tostring(self):
        return "(" + str(self.value) + " : " + str(self.type) + ")"
    __str__ = tostring
    __repr__ = tostring

#
# PHRASE
#
class Phrase:

    def __init__(self, values):
        self.values = values

    def get_result(self):
        return self.values[-1]

    def tostring(self):
        s = "[ "
        for v in self.values: s += str(v) + " "
        s += "]"
        return s
    __str__ = tostring
    __repr__ = tostring

#
# ARGUMENT
#
class Argument:

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def tostring(self):
        return self.name + " : " + (str(self.type) if self.type else "Any")
    __str__ = tostring
    __repr__ = tostring

#
# CONTEXT
#
class Context:

    def __init__(self):
        self.lets = []
        self.constants = []
        self.functions = []
        self.invocations = []

    def add(self, x):
        if isinstance(x, Let):
            self.lets.append(x)
        elif isinstance(x, Constant):
            self.constants.append(x)
        elif isinstance(x, Function):
            self.functions.append(x)
        elif isinstance(x, Invocation):
            self.invocations.append(x)

    def tostring(self):
        s = ""
        def section(title):
            return ("---------------------\n" +
                title + "\n"
                "---------------------\n")
        # lets
        s += section("lets:")
        for x in self.lets: s += str(x) + "\n"
        # constants
        s += section("constants:")
        for x in self.constants: s += str(x) + "\n"
        # functions
        s += section("functions:")
        for x in self.functions: s += str(x) + "\n"
        # invocations
        s += section("invocations:")
        for x in self.invocations: s += str(x) + "\n"

        return s
    __str__ = tostring
    __repr__ = tostring

#
# PARSE
#
def parse(lexed):

    context = Context()

    # args can have specified types
    def parse_arg(arg):
        if arg[0].startswith("~\\"):
            if len(arg) < 2:
                logger.log("error", "after the type judgement of an argument to a function, you must provide a name for the argument.")
                return "error"
            type = FunctionReference(arg[0][2:])
            name = arg[1]
            argument = Argument(name, type)
            return argument
        else:
            name = arg[0]
            argument = Argument(name, None)
            return argument

    # for phrases
    def parse_phrase(arr):
        phrase = [parse_helper(x) for x in arr]
        return Phrase(phrase)

    # for when you need a phrase to return a value
    def parse_result(arr):
        return parse_phrase(arr).get_result()

    def parse_invocation(invo):
        # let a Constant
        if builtins["let"] == invo.name:
            if len(invo.args) % 2 != 0:
                logger.log("error", "for each name provided to `let`, there must be an immediately following value to bind it to.")
                return "error"
            name = parse_result(invo.args[0])
            type = parse_result(invo.args[1])
            let = Let(name, type)
            context.add(let)
            return let

        # set a Constant
        elif builtins["set"] == invo.name:
            if len(invo.args) % 2 != 0:
                logger.log("error", "for each name provided to `set`, there must be an immediately following value to bind it to.")
                return "error"
            name = parse_result(invo.args[0])
            value = parse_helper(invo.args[1])
            cons = Constant(name, value)
            context.add(cons)
            return cons
        
        # define a Function
        # opens a new context
        elif builtins["function"] == invo.name:
            if len(invo.args) < 2:
                logger.log("error", "to define a function you must at least provide a name and a result.")
                return "error"
            name = parse_result(invo.args[0])
            args = [parse_arg(x) for x in invo.args[1:-1]]
            result = parse_result(invo.args[-1])
            func = Function(name, args, result)
            context.add(func)
            return func

        # invoke a normal function
        else:
            name = invo.name
            args = [parse_result(x) for x in invo.args]
            invocation = Invocation(name, args)
            context.add(invocation)
            return invocation


    def parse_constantreference(cref):
        # have name and thats all
        name = cref.name
        consref = ConstantReference(name)
        context.add(consref)
        return consref

    def parse_functionreference(fref):
        # have a name and thats all
        name = fref.name
        funcref = FunctionReference(name)
        context.add(funcref)
        return funcref


    def parse_helper(x):
        if isinstance(x, lexer.FunctionInvocation):
            return parse_invocation(x)
        elif isinstance(x, lexer.ConstantReference):
            return parse_constantreference(x)
        elif isinstance(x, lexer.FunctionReference):
            return parse_functionreference(x)
        elif isinstance(x, list):
            return parse_phrase(x)
        elif isinstance(x, str):
            return Value(x, "String")
        else:
            return "error: " + str(x)

    for x in lexed.args[0]:
        logger.log("log",x)
        parse_helper(x)

    # print(context)
