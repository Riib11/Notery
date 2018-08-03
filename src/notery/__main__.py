import notery.parsing.parser as parser
import notery.parsing.lexer as lexer
import notery.cmdline.logger as logger
import notery.cmdline.titler as titler

import argparse
import sys
import subprocess

def main():

    # argument parser
    argparser = argparse.ArgumentParser()
    
    # arguments: positional
    argparser.add_argument("mode", help="[ html | pdf | update | info ]")
    argparser.add_argument("input", nargs="?", help="input file")

    # argument: optional
    argparser.add_argument("-o","--output", help="name for the output file")
    argparser.add_argument("-d","--debug", help="print debug logs", action="store_true")
        
    # parse arguments
    args = argparser.parse_args()
    # logger.log( "log" , args )

    def check_input():
        if not args.input:
            logger.log( "error" , "please provide an input .nty file" )
            quit()

    #
    # compile
    #
    if "html" == args.mode or "pdf" == args.mode:

        check_input()
        with open(args.input, "r+") as file:
            string = "".join([ l for l in file ])
            lexed = lexer.lex(string)
            parsed = parser.parse(lexed)
            # logger.log("log", parsed)

            # output html
            if "html" == args.mode: pass
            # output pdf
            elif "pdf" == args.mode: pass

    #
    # update from github
    #
    elif "update" == args.mode:

        # TODO
        logger.log( "msg" , "to update Notery, please run `sh .../Notery/update.sh`" )
        # subprocess.call(["sh","~/git/Notery/install.sh"])

    #
    # get info
    #
    elif "info" == args.mode:

        titler.print_title()

    #
    # invalid mode
    #
    else:

        logger.log( "error" , "'"+args.mode+"' is not a valid mode" )



#
#
#
main()