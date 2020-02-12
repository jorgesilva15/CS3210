# CS3210 - Principles of Programming Languages - Spring 2020
# A recursive-descent parser for an expression

from enum import IntEnum
import sys

# all char classes
class CharClass(IntEnum):
    EOF        = -1
    LETTER     = 1
    DIGIT      = 2
    OPERATOR   = 3
    PUNCTUATOR = 4
    QUOTE      = 5
    BLANK      = 6
    DELIMITER  = 7
    OTHER      = 8

# all tokens
class Token(IntEnum):
    EOF             = -1
    ADDITION        = 1
    SUBTRACTION     = 2
    MULTIPLICATION  = 3
    DIVISION        = 4
    IDENTIFIER      = 5
    LITERAL         = 6

# lexeme to token conversion map
lookupToken = {
    "$"         : Token.EOF,
    "+"         : Token.ADDITION,
    "-"         : Token.SUBTRACTION,
    "*"         : Token.MULTIPLICATION,
    "/"         : Token.DIVISION
}

# a tree-like data structure
class Tree:

    TAB = "   "

    def __init__(self):
        self.data     = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

# error code to message conversion function
def errorMessage(code):
    msg = "Error " + str(code).zfill(2) + ": "
    if code == 1:
        return msg + "source file missing"
    if code == 2:
        return msg + "couldn't open source file"
    if code == 3:
        return msg + "lexical error"
    if code == 4:
        return msg + "couldn't open grammar file"
    if code == 5:
        return msg + "couldn't open SLR table file"
    if code == 6:
        return msg + "EOF expected"
    if code == 7:
        return msg + "identifier expected"
    if code == 8:
        return msg + "special word missing"
    if code == 9:
        return msg + "symbol missing"
    if code == 10:
        return msg + "data type expected"
    if code == 11:
        return msg + "identifier or literal value expected"
    return msg + "syntax error"

# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '"':
        return (c, CharClass.QUOTE)
    if c in ['+', '-', '*', '/']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    if c in ['(', ')']:
        return (c, CharClass.DELIMITER)
    return (c, CharClass.OTHER)

# calls getChar and addChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

# returns the next (lexeme, token) pair or ("", EOF) if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # checks EOF
    if charClass == CharClass.EOF:
        return (input, lexeme, Token.EOF)

    # reads an identifier
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER or charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, Token.IDENTIFIER)

    # reads digits
    if charClass == CharClass.DIGIT:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, Token.LITERAL)

    # reads operator
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookupToken:
            return (input, lexeme, lookupToken[lexeme])

    # anything else, raises an error
    raise Exception(errorMessage(3))

# parse
def parse(input):

    # TODOd: create the parse tree
    tree = Tree()

    # call parse expression
    parseExpression(input, tree)

    # return the parse tree
    return tree

# <expression>  -> <term> <expression’>
# <expression'> -> (+|-) <term> <expression'>
# <expression'> -> epsilon
def parseExpression(input, tree):

    # TODOd: update the tree's root with the label <expression>
    tree.data = "<expression>"


    # TODOd: call parse a term
    input, lexeme, token = parseTerm(input, tree)


    # parse more terms
    while True:
        # TODOd: if current token is + or - then add the lexeme to the tree and call parse term again
        if token == Token.ADDITION or token == Token.SUBTRACTION:
            tree.add(lexeme)
            input, lexeme, token = parseTerm(input, tree)

        # TODOd: check for EOF
        elif token == Token.EOF:
            break

        # TODOd: raise an exception
        else:
            raise Exception(errorMessage(6))


# <term> -> <factor> <term’>
# <term'> -> (*|/) <factor> <term'>
# <term'> -> epsilon
def parseTerm(input, tree):

    # TODOd: create a subtree with the label <term>
    subTree = Tree()
    subTree.data = "<term>"


    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # TODOd: call parse a factor
    input, lexeme, token = parseFactor(input, subTree)

    # parse more factors
    while True:
        # TODOd: if current token is * or / then add the lexeme to the tree and call parse factor again
        if token == Token.MULTIPLICATION or token == Token.DIVISION:
            subTree.add(lexeme)
            input, lexeme, token = parseFactor(input, subTree)

        # TODO: anything different than * or / then break the loop
        else:
            break

    # TODOd: return input, lexeme, token
    return input, lexeme, token

# <factor> -> <identifier> | <literal>
def parseFactor(input, tree):

    # TODOd: create a subtree with the label <factor>
    subTree = Tree()
    subTree.data = "<factor>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # TODOd: read a token
    input, lexeme, token = lex(input)

    # TODOd: if token is an identifier or literal, add the lexeme as child of subTree and read the next token
    if token == Token.IDENTIFIER or token == Token.LITERAL:
        subTree.add(lexeme)
        input, lexeme, token = lex(input)

    # TODOd: anything different than identifier or literal, raise an exception
    else:
        raise Exception(errorMessage(11))


    # TODOd: return input, lexeme, token
    return input,lexeme, token

# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # calls the parser function
    tree = parse(input)

    # prints the tree if the code is syntactically correct
    if tree:
        print("Input is syntactically correct!")
        print("Parse Tree:")
        tree.print()
    else:
        # prints error message otherwise
        print("Code has syntax errors!")
