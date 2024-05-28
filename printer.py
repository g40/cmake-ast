# /cmakeast/printer.py
#
# Dumps an AST for a specified FILE on the commandline
#
# See /LICENCE.md for Copyright information
"""Dump an AST for a specified FILE on the commandline."""

import argparse

import sys

from cmakeast import ast
from cmakeast import ast_visitor
from utils.dbmsg import dbmsg

#------------------------------------------------------------------------------
#
def defineMacro(node, symtab:dict):
    # semantic processing
    if node.name == "SET":
        args = node.arguments
        if len(args) == 2 and symtab is not None:
            # var = literal
            key = args[0].contents
            val = args[1].contents
            try:
                symtab[key] = val
            except:
                pass
    #
    return node, symtab

#------------------------------------------------------------------------------
# has to be an include node                                                         
def applyMacro(node, symtab:dict):                                     
    # ${ProjDirPath}/flags.cmake
    s:str = node.Filename
    si:int = s.find("${")
    ei:int = 0
    if si >= 0:
        # skip ${}
        ei = s.find("}",si+2)
        # get the key
        k:str = s[si+2:ei]
        k2:str = s[si:ei+1]
        #
        try:
            # lookup the value for the key
            v:str = symtab[k]
            # replace
            s2:str = s.replace(k2,v)
            #
            # dbmsg.debug(f"Macro: {s} => {s2}")
            #
            node.Filename = s2
        except:
            pass
    # *must* return something, else Python will.
    return node

#------------------------------------------------------------------------------
#
def _parse_arguments():
    """Return a parser context result."""
    parser = argparse.ArgumentParser(description="CMake AST Dumper")
    parser.add_argument("filename", nargs=1, metavar=("FILE"), help="read FILE")
    return parser.parse_args()


#------------------------------------------------------------------------------
#
def _print_details(extra=None):
    """Return a function that prints node details."""
    def print_node_handler(name, node, depth, symtab) -> dict:
        """Standard printer for a node."""

        ind:str = (" " * depth)
        s = f"{ind} {name} ({node.line}:{node.col})"
        if extra is not None:
            s += " [{0}]".format(extra(node))
        dbmsg.debug(s)

        return symtab

    return print_node_handler

#------------------------------------------------------------------------------
# JME
def _print_function_call(extra=None):

    """Return a function that prints node details."""
    def print_function_call_handler(name, node, depth, symtab:dict) -> dict:
        """Standard printer for a node."""

        ind:str = (" " * depth)
        # s = f"{ind} {name}:{node.name} => {node.arguments} {len(node.arguments)} ({node.line}:{node.col})"
        s = f"{ind} {name}:{node.name} => arity:{len(node.arguments)} ({node.line}:{node.col})"
        if extra is not None:
            s += " [{0}]".format(extra(node))
        dbmsg.debug(s)

        """
        line = "{0}{1} {2} ({3}:{4})".format(depth,
                                             (" " * depth),
                                             name,
                                             node.line,
                                             node.col)
        if extra is not None:
            line += " [{0}]".format(extra(node))
        #
        dbmsg.debug(line)
        """
        #
        node,symtab = defineMacro(node,symtab)
        #
        return symtab

    # return a function
    return print_function_call_handler

#------------------------------------------------------------------------------
# JME
def _print_include(extra=None):

    """Return a function that prints node details."""

    def print_include_handler(name:str, node, depth:int, symtab:dict) -> dict:

        # do macro stuff
        node = applyMacro(node,symtab)

        """Standard printer for a node."""
        line = "{0}{1} {2} {3} ({4}:{5})".format(depth,
                                             (" " * depth),
                                             name,
                                             node.Filename,
                                             node.line,
                                             node.col)
        if extra is not None:
            line += " [{0}]".format(extra(node))
        #   
        dbmsg.debug(line)

        return symtab
    
    # return a function
    return print_include_handler

#------------------------------------------------------------------------------
# handles includes
def do_print(filename):

    """Print the AST of filename."""

    with open(filename) as ipfile:
        #
        body = None
        # dictionary
        symtab = dict()
        #
        word_print = _print_details(lambda n: "{0} {1}".format(n.type,n.contents))
        #
        if True:
            contents = ipfile.read()
            body = ast.parse(contents,body, symtab)
            
            # dbmsg.debug(f"{body} {body.statements}")
            # ast_visitor.recurse(body,include=_print_include())
                                
            ast_visitor.recurse(body,
                                symtab,
                                while_stmnt=_print_details(),
                                foreach=_print_details(),
                                function_def=_print_details(),
                                macro_def=_print_details(),
                                if_block=_print_details(),
                                if_stmnt=_print_details(),
                                elseif_stmnt=_print_details(),
                                else_stmnt=_print_details(),
                                include=_print_include(),
                                #function_call=_print_details(lambda n: n.name),
                                function_call=_print_function_call(),
                                word=word_print)

            dbmsg.debug("Macros------------------------------------------------")
            for k,v in symtab.items():
                try:
                    dbmsg.debug(f"Symbol: {k} = {v}")
                except:
                    pass

        dbmsg.debug("------------------------------------------------------")
        if False:
            body2 = ast.parse_ex(filename)
            ast_visitor.recurse(body2,
                                while_stmnt=_print_details(),
                                foreach=_print_details(),
                                function_def=_print_details(),
                                macro_def=_print_details(),
                                if_block=_print_details(),
                                if_stmnt=_print_details(),
                                elseif_stmnt=_print_details(),
                                else_stmnt=_print_details(),
                                include=_print_details(lambda n: n.filename),
                                function_call=_print_details(lambda n: n.name),
                                word=word_print)

#------------------------------------------------------------------------------
#
def main():
    """Parse the filename passed on the commandline and dump its AST.

    The AST will be dumped in tree form, with one indent for every new
    control flow block
    """
    result = _parse_arguments()
    do_print(result.filename[0])

#--------------------------------------------------------------------
if __name__ == "__main__":
    main()
