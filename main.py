import Lexer #Import the lexer

print('\n\n')
print(">> VIEW THE README.md <<") # Tell everyone to read the Readme
print('\n\n\n\n')

text = open("test.lang").read() #Read some code from test.lang
Language = Lexer.Lexer("//", "</", "/>", False, False) # Initilize the Lexer

Language.tokenize(text) # Tokenize the data
print(Language.output) #Print the output.