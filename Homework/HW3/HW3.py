# CS3210 - Principles of Programming Languages - Spring 2020
# A Lexical Analyzer for expressions

from enum import Enum
import sys

# all char classes
class CharClass(Enum):
    EOF        = 1
    LETTER     = 2
    DIGIT      = 3
    OPERATOR   = 4
    PUNCTUATOR = 5
    QUOTE      = 6
    BLANK      = 7
    OTHER      = 8

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
    if c in ['$']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ':', ',', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    return (c, CharClass.OTHER)

# calls getChar and getChar until it returns a non-blank
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

# all tokens
class Token(Enum):
    DECLARE     = 1
    IDENTIFIER     = 3
    REAL     = 4
    COMPLEX = 5
    FIXED    = 6
    FLOATING   = 7
    SINGLE  = 8
    DOUBLE = 9
    BINARY = 10
    DECIMAL = 11

# lexeme to token conversion
lookup = {
    "declare"      : Token.DECLARE,
    "$"      : Token.IDENTIFIER,
    "real"      : Token.REAL,
    "fixed"      : Token.FIXED,
    "floating"      : Token.FLOATING,
    "single"      : Token.SINGLE,
    "double"    : Token.DOUBLE,
    "binary"    : Token.BINARY,
    "decimal"   : Token.DECIMAL
}

# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return (input, None, None)

    # TODOd: read a $ followed by letters
    if charClass == CharClass.QUOTE:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, Token.IDENTIFIER)
    #read a letter followed by letters
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, lookup[lexeme])

    # TODOd: read an operator
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookup:
            return (input, lexeme, lookup[lexeme])

    #TODOd: read open/close parenthesis
    if charClass == CharClass.OTHER:
        if c == '(' or c == ')':
            input, lexeme = addChar(input, lexeme)
        return (input, lexeme, lookup[lexeme])

    # TODOd: anything else, raise an exception
    raise Exception("Lexical Analyzer Error: unrecognized symbol found!")

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

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme == None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
