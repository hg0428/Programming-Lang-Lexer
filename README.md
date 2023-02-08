### Have you ever wanted to build a programming language?
Well, heres a great start. This is a lexer that you can configure to your needs! 

You can use it to build a variety of projects from a syntax highlighter to a programming language.


## How to use:
In main.py, you can change the arguments given to Lexer to adjust the languages syntax.

The first argument is the start sequence for single line comments. They end at the end of the line.

The second argument is the start sequence for multiline comments. 

The third argument are the characters that end a multiline comment.

The fourth argument tells the lexer whether to count indents as tokens. This is useful if you are creating a language like Python.

The fith argument tells the lexer whether to tokenize comments, this is useful if you are creating a syntax highlighter where you need to recognize comments.

## Further configuration:
In Data.py, you can configure all the variables to fit your needs. You can add new keywords, new operators, new delimiters, new whitespace charcters, new endlines, and really whatever you need.

The variables are Sets, Sets filter out duplicates.

## Editting the Lexer:
You can customize the lexer by changing Lexer.py. If you would like to add a new type of tokens, for example, Booleans, this is how you would do this:
First, in Data.py, you would create a Set called `Booleans`.
```py
Booleans = {
  'true',
  'false'
}
```
Then you would add a new TokenType, `Boolean` to the `TokenTypes` dict.
```py
TokenTypes = {
    "String": TokenType("String"),
    "Number": TokenType("Number"),
    "Keyword": TokenType("Keyword"),
    "Operator": TokenType("Operator"),
    "Identifier": TokenType("Identifier"),
    "Delimiter": TokenType("Delimiter"),
    "Indent": TokenType("Indent"),
    "Comment": TokenType("Comment"),
    "LineBreak": TokenType("LineBreak"),
    "Boolean": TokenType("Boolean") #Added Boolean
}
```
Then, in Lexer.py, you would check if an identifier is in `Booleans`. So, first, import the `Booleans` set.
```py
from Data import TokenTypes, Operators, Keywords, Quotes, Whitespaces, PureOperators, Delimiters, Newlines, Booleans
```
Then on line 239, you would add the check and then add the token.
```py
if value in Booleans:
    self.addToken("Boolean",
                start,
                self.index,
                self.line,
                startcolumn,
                self.column,
                value)
```
Now, Bools are implemted!

These are the basic steps you would need to follow to add anything into this lexer.


## Building projects from it:
I have built a terminal syntax highlighter based on this template, and I will publish it soon!

Also working on a new Aardvark version, also based on this template.

Copy and edit this code and customize it to your needs to build whatever you need. 

🙂 **I can't wait to see the projects you build with this!** 🎉
## If you enjoyed this...
Please join my programming discord server: https://discord.com/invite/KqhqnHrrZJ

And... follow me for a Parser Template!