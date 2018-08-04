from notery.utility.strings import *
import notery.cmdline.logger as logger

#
# FUNCTION functioninvocation
#
class FunctionInvocation:

    def __init__(self, parent=None, name=None):
        self.parent = parent
        self.name = name
        self.args = []

        if self.parent:
            parent.add(self)

    def start_arg(self):
        self.args.append([])
    
    def add(self, x):
        if len(self.args) == 0:
            self.start_arg()
        self.args[-1].append(x)

    def tostring(self):
        s = "(." + (self.name if self.name else "_") + " : "
        for arg in self.args:
            s += str(" ".join([str(a) for a in arg])) + " | "
        if s.endswith(" | "): s = s[:-3]
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
        return "->" + self.name
    __str__ = tostring
    __repr__ = tostring

#
# CONSTANT REFERENCE
#
class ConstantReference:

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return "$" + self.name
    __str__ = tostring
    __repr__ = tostring


def lex(string):
    string = rreplace( string , "\n" , " " )
    string = rreplace( string , "  ", " " )
    words = string.split(" ")

    in_comment = False
    functioninvocation = FunctionInvocation(name="__main")
    for w in words:

        if len(w)==0: continue

        # end current comment
        elif in_comment:
            in_comment = not w.startswith("\\")
        
        # comment start
        elif w.startswith("\\.*"):
            in_comment = True

        # end current functioninvocation
        elif w.startswith("\\\\"):
            functioninvocation = functioninvocation.parent
        
        # start new functioninvocation as child
        elif w.startswith("\\."):
            functioninvocation = FunctionInvocation(functioninvocation, w[2:])

        # reference to command word
        elif w.startswith("~\\"):
            reference = FunctionReference(w[2:])
            functioninvocation.add(reference)
            
        # start new arg
        elif w.startswith("|"):
            functioninvocation.start_arg()

        elif w.startswith("\\"):
            const = ConstantReference(w[1:])
            functioninvocation.add(const)

        # add argument text
        else:
            functioninvocation.add(w)

    return functioninvocation
