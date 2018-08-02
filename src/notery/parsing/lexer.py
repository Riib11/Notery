def lex(string):
    while "\n" in string:  string = string.replace("\n","")
    while "  " in string: string = string.replace("  "," ")
    ls = string.split("\\")
    first = True
    for x in ls: print(("\\" if not first else "")+str(x)); first = False

    

with open("/Users/Henry/git/Notery/examples/test/test2.nty") as file:
    string = "".join([ l for l in file ])
    lexed = lex(string)

