from notery.utility.strings import *

#
# BLOCK
#
class Block:

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
# CONSTANT
#
class Constant:

    def __init__(self, name):
        self.name = name

    def tostring(self):
        return "\\" + self.name

    __str__ = tostring
    __repr__ = tostring


def lex(string):
    string = rreplace( string , "\n" , " " )
    string = rreplace( string , "  ", " " )
    words = string.split(" ")
    # print(words)

    block = Block()
    for w in words:
        # print(block)
        
        # end current block
        if w.startswith("\\\\"):
            block = block.parent
        
        # start new block
        elif w.startswith("\\."):
            block = Block(block, w[2:])

        # reference to command word
        elif w.startswith("~\\"):
            block.add(w)
            
        # start new arg
        elif w.startswith("|"):
            block.start_arg()

        elif w.startswith("\\"):
            const = Constant(w[1:])
            block.add(const)

        # add argument text
        else:
            if len(w) > 0: block.add(w)

    print(block)

with open("/Users/Henry/git/Notery/examples/test/test2.nty") as file:
    string = "".join([ l for l in file ])
    lexed = lex(string)