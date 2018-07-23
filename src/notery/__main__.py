from notery.cmdline.logger import log
from notery.cmdline.title import print_title

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
    # print("args:",args)

    #
    # compile to html
    #
    if "html" == args.mode:

        if not args.input: log( "error" , "please provide an input .nty file" )

    #
    # compile to pdf
    #
    elif "pdf" == args.mode:

        if not args.input: log( "error" , "please provide an .nty notery file" )

    #
    # update from github
    #
    elif "update" == args.mode:

        subprocess.run([".","/git/Notery/install.sh"])

    #
    # get info
    #
    elif "info" == args.mode:

        print_title()

    #
    # invalid mode
    #
    else:

        log( "error" , "'"+args.mode+"' is not a valid mode" )



#
#
#
main()