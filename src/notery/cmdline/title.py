from notery.cmdline.printcolor import *

def repeat(n,f):
    for _ in range(n): f()

def fill( n=1 ):
    repeat(n, lambda:
        printc(" ", back=PrintStyle.BACK_cyan, end=""))

def space( n=1 ): 
    repeat(n, lambda:
        printc(" ", back=PrintStyle.BACK_black, end=""))

def shadow_h( n=1 ):
    repeat(n, lambda: printc("═", spec=2, back=PrintStyle.BACK_black, end=""))

def shadow_v( n=1 ):
    repeat(n, lambda: printc("║", spec=2, back=PrintStyle.BACK_black,  end=""))

def shadow_cbl( n=1 ):
    repeat(n, lambda: printc("╝", spec=2, back=PrintStyle.BACK_black,  end=""))

def shadow_ctr( n=1 ):
    repeat(n, lambda: printc("╔", spec=2, back=PrintStyle.BACK_black,  end=""))

def shadow_ctl( n=1 ):
    repeat(n, lambda: printc("╗", spec=2, back=PrintStyle.BACK_black,  end=""))

def shadow_t( n=1 ):
    repeat(n, lambda: printc("╦", spec=2, back=PrintStyle.BACK_black,  end=""))

def shadow(): printc(" ", spec=2, back=PrintStyle.BACK_black, font=PrintStyle.FONT_white, end="")

def br( n=1 ):
    repeat(n, lambda:
        print())

"""
left bottom  : ▖

left top     : ▘

right bottom : 

right top    :




"""

def shape( ss ):
    for s in ss:
        for c in s:
            if   c == "#": fill()
            elif c == " ": space()
            elif c == "-": shadow_h()
            elif c == "|": shadow_v()
            elif c == "/": shadow_cbl()
            elif c == "^": shadow_ctr()
            elif c == "]": shadow_ctl()
            elif c == "T": shadow_t()
            else: printc(c, spec=2, back=PrintStyle.BACK_black, font=PrintStyle.FONT_white, end="")
        br()


def print_title():

    shape([
        "",
        "###   ##   ######   ########   ######   #######   ##    ##",
        "####  ##| ###^-###  #^-##T-#] ##^---##] ##^---##  ##|   ##|",
        "##|## ##| ##^/  ##|    ##|    #####  -/ #######|   ######^/",
        "##| ####| ###  ###|    ##|    ##^-- ##  ##|  ##╚]    ##^-/  ",
        "##|  ###|  ######^/    ##|     ######^/ ##|  ╚##|    ##|  ",
        "--/   --/   -----/      -/      -----/   -/    -/     -/"
        "",""
    ])