from notery.utility.strings import *
import notery.cmdline.logger as logger

#
# INVOCATION
#
class Invocation:

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
# REFERENCE
#
class Reference:

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return "->" + self.name
    __str__ = tostring
    __repr__ = tostring

#
# CONSTANT
#
class Constant:

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
    # print(words)

    in_comment = False
    invocation = Invocation(name="__main")
    for w in words:
        # print(invocation)

        if len(w)==0: continue

        # end current comment
        elif in_comment:
            in_comment = not w.startswith("\\")
        
        # comment start
        elif w.startswith("\\.*"):
            in_comment = True

        # end current invocation
        elif w.startswith("\\\\"):
            invocation = invocation.parent
        
        # start new invocation as child
        elif w.startswith("\\."):
            invocation = Invocation(invocation, w[2:])

        # reference to command word
        elif w.startswith("~\\"):
            refer = Reference(w[2:])
            invocation.add(refer)
            
        # start new arg
        elif w.startswith("|"):
            invocation.start_arg()

        elif w.startswith("\\"):
            const = Constant(w[1:])
            invocation.add(const)

        # add argument text
        else:
            invocation.add(w)

    return invocation
