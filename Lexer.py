from Data import TokenTypes, Operators, Keywords, Quotes, Whitespaces, PureOperators, Delimiters, Newlines


class Token:
    def __init__(self,
                 toktype,
                 start: int,
                 end: int,
                 line: int,
                 columnstart: int,
                 columnend: int,
                 value=None,
                 variation=None):
        if type(toktype) == str:
            toktype = TokenTypes[toktype]
        self.columnstart = columnstart  #The column the token starts on
        self.columnend = columnend  #The column the token ends on
        self.type = toktype  #The type of the token, this is a TokenType object
        self.length = end - start  #The length of the token.
        self.start = {"line": line, "col": columnstart}
        self.end = {"line": line, "col": columnend}
        self.start_index = start  #The index of the first character of the token.
        self.end_index = end  # Ther index of the last character of the token.
        self.value = value
        self.line = line  #The line numbe the token is on
        self.variation = variation  #The variation would be like the type of quote

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', from {self.start['line']}:{self.start['col']} to {self.end['line']}:{self.end['col']})"
        # To make it look neat when we print it.


class Lexer:
    def __init__(self,
                 singleline: str,
                 multilines: str,
                 multilinee: str,
                 useIndents=False,
                 tokenizeComments=False):
        self.useIndents = useIndents  #Whether to use indents or not
        self.comment = singleline  # The syntax to start a comment (eg, # for python)
        self.commentstart = multilines  # The syntax to start a multiline comment (eg, /* for JS)
        self.commentend = multilinee  # The syntax to end a multiline comment (eg, */ for JS)
        self.tokenizeComments = tokenizeComments  #Whether or not to turn comments into tokens. If False, comments will be ignored.
        self.data = ""  # The code.
        self.index = 0  #The index of the character the Lexer is currently on.
        self.line = 1  # The line number the Lexer is currently on in the proccess of generating tokens
        self.column = 1  #The column number the Lexer is currently on
        self.output = []  #The generated tokens
        self.empty = True  #Whether or not a linebreak was the last token. If so, notice indents
        self.AtEnd = False  #Whether or not we are at the end of the file
        self.curChar = ""  #The current character

    def isWhitespace(self, char=None):  #Check if the character is a whitespace
        char = char or self.curChar  #If char is not specified, then use the current character
        return char in Whitespaces

    def isNewline(self, char=None):  #Check if the character is a newline
        char = char or self.curChar
        return char in Newlines

    def isQuote(self, char=None):  #Check if the character is a quote
        char = char or self.curChar
        return char in Quotes

    def isDelimiter(self, char=None):  #Check if the character is a delimiter
        char = char or self.curChar
        return char in Delimiters

    def detect(self, text):  #Detect if text starts at the currect character.
        if self.curChar != text[0]:
            return False
        return all(self.peek(i + 1) == text[i + 1] for i in range(len(text) - 1))

    def isNumber(self, char=None):  #Check if the character is a number
        char = char or self.curChar
        return (char in "0123456789")

    def addToken(self, *args, **kwargs):  #Add a token to the output
        self.output.append(Token(*args, **kwargs))
        self.empty = False

    def otherwise(self, char=None): #If its nothing else, then its an identifier.
        char = char or self.curChar
        return not (self.isWhitespace(char) or self.isDelimiter(char)
                    or self.isNewline(char) or self.isQuote(char)
                    or self.isNumber(char) or char == self.comment
                    or char in PureOperators)

    def newline(self): #Handle the \n
        #Self.empty means that we are on an empty line
        self.empty = True
        self.line += 1
        self.column = 1

    def tokenize(self, data: str):
        """
        Takes code and converts it to tokens.
        """
        if not data: #Return output if no code was given to tokenize.
            return self.output
        self.data += data #Add the given code to self.data.
        self.curChar = self.data[self.index] #Set the current character to the current character.
        while self.index < len(self.data): #Loop through the text until its over.

            #Newlines (\n or ;)
            if self.isNewline():
                self.addToken('LineBreak',
                              start=self.index,
                              end=self.index,
                              line=self.line,
                              value=self.curChar,
                              variation=self.curChar,
                              columnstart=self.column,
                              columnend=self.column)
                if self.curChar == '\n':
                    self.newline()  #Only incremnet the line if its a \n
                else:
                    self.empty = True

            #Indents
            elif self.isWhitespace() and self.empty and self.useIndents:
                value = ''
                start = self.index
                startcolumn = self.column
                while self.isWhitespace() and not self.AtEnd:
                    value += self.curChar
                    self.advance()
                if not self.isNewline():
                    self.advance(-1)
                    self.addToken("Indent",
                                  start,
                                  self.index,
                                  self.line,
                                  value=value,
                                  columnstart=startcolumn,
                                  columnend=self.column)
                else:
                    self.advance(-1)

            #Delimiters
            elif self.isDelimiter():
                self.addToken("Delimiter", self.index, self.index, self.line,
                              self.column, self.column, self.curChar)

            #Numbers
            elif self.isNumber():
                start = self.index
                startcolumn = self.column
                value = ''
                seen_dot = False
                while (self.isNumber()
                       or self.curChar == ".") and not self.AtEnd:
                    if seen_dot and self.curChar == ".":
                        raise Exception(
                            "invalid syntax, floats can only have one '.'")
                    if self.curChar == ".": seen_dot = True
                    value += self.curChar
                    self.advance()

                self.advance(-1)
                self.addToken("Number", start, self.index, self.line,
                              startcolumn, self.column, value)

            #Single line comments
            elif self.detect(self.comment):
                value = ""
                start = self.index
                startcolumn = self.column
                while not self.isNewline() and not self.AtEnd:
                    value += self.curChar
                    self.advance()
                if self.tokenizeComments:
                    self.addToken("Comment", start, self.index, self.line,
                                  startcolumn, self.column, value)
                self.advance(-1)  #To register the new line

            #Multi-line comments
            elif self.detect(self.commentstart):
                value = ""
                start = self.index
                startcolumn = self.column
                while not self.detect(self.commentend) and not self.AtEnd:
                    value += self.curChar
                    self.advance()
                if self.tokenizeComments:
                    self.addToken("Comment", start, self.index, self.line,
                                  startcolumn, self.column, value)
                self.advance(len(self.commentend))  # To skip past the />

            #Strings
            elif self.isQuote():
                variation = self.curChar
                value = ""
                begin = self.index
                startcolumn = self.column
                while not self.AtEnd:
                    self.advance()
                    if (self.curChar == variation
                            and value[-1] != '\\') or self.AtEnd:
                        break
                    value += self.curChar

                self.addToken("String", begin, self.index, self.line,
                              startcolumn, self.column, value, variation)

            #Operators
            elif self.curChar in PureOperators:
                #If the current character is one of the non-word operators
                value = ''
                start = self.index
                startcolumn = self.column
                while not self.AtEnd and (value + self.curChar) in Operators:
                    value += self.curChar
                    self.advance()
                self.advance(-1)  #Go back to a valid character
                self.addToken("Operator", start, self.index, self.line,
                              startcolumn, self.column, value)

            #Identifiers, Keywords, and Operators.
            elif self.otherwise():
                value = ''
                start = self.index
                startcolumn = self.column
                while self.otherwise() and not self.AtEnd:
                    value += self.curChar
                    self.advance()
                self.advance(-1)
                if value in Operators:
                    self.addToken("Operator", start, self.index, self.line,
                                  startcolumn, self.column, value)
                elif value in Keywords:
                    self.addToken("Keyword", start, self.index, self.line,
                                  startcolumn, self.column, value)
                else:
                    self.addToken("Identifier",
                                  start,
                                  self.index,
                                  self.line,
                                  columnstart=startcolumn,
                                  columnend=self.column,
                                  value=value)

            if self.AtEnd: break
            self.advance()  #Next character and continue the loop
        return self.output #Return the generated tokens

    def advance(self, amt=1): #Advance amt characters forward in the code
        self.index += amt #Increase the index
        self.column += amt #Increase the columns
        if self.index < len(self.data): # If we haven't reached the end yet
          self.curChar = self.data[self.index] #Then set the current character
        else: #Otherwise, set AtEnd to true
          self.AtEnd = True

    def peek(self, amt=1): #Look at a character that is ahead in the text.
        if self.index + amt < len(self.data):
            return self.data[self.index + amt]
        else:
            return None
