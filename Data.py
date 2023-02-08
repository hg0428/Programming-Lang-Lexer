class TokenType:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


TokenTypes = {
    "String": TokenType("String"),
    "Number": TokenType("Number"),
    "Keyword": TokenType("Keyword"),
    "Operator": TokenType("Operator"),
    "Identifier": TokenType("Identifier"),
    "Delimiter": TokenType("Delimiter"),
    "Indent": TokenType("Indent"),
    "Comment": TokenType("Comment"), # Having comment tokens is useful for syntax highlighters. But, this is only enabled if enabled in the Lexer's __Init__ method.
    "LineBreak": TokenType("LineBreak"),
} #These are the types of tokens the lexer can return.

PureOperators = {
    "=",
    "+",
    "-",
    "/",
    "*",
    "^",
    "%",
    "!",
    "<",
    ">",
    "==",
    "<=",
    ">=",
    "!=",
    "&&",
    "||",
    "x|",
} # These are symbol based operators.


Operators = PureOperators | {
  'not', 
  'and', 
  'or'
}  # Keyword based operators


Quotes = {'"', "'", '`'} # The types of quotes that can be used.


Whitespaces = {
    ' ',  #Space
    '\t',  #Tab
} # Characters to be counted in an indent


Delimiters = {
    ":",  #Colon, used for defining blocks and for types
    "(",  #lparen
    ")",  #rparen
    ",",  #comma
    "{",  #lbrace
    "}",  #rbrace
    "[",  #lbracket
    "]",  #rbracket
    ".",  #period,
} #Delimiters that aren't operators, but that the Lexer needs to distinguish.

Keywords = {
  "say", 
  "input", 
  "if", 
  "while", 
  "for", 
  "do",
  "return",
  "func",
  "def"
} # These are the keywords.

Newlines = {
  '\n', 
  ';'
} # These characters are line breaks, although only \n will increment the line number
