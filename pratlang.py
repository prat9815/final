#Showing all the digits that are there 
digi = '0123456789'

#If there is a character that is not in the token type then produce an error
class Error:
    def __init__(self,error_name, details):
       
        self.error_name = error_name
        self.details = details
    
    def as_string(self):
        result  = f'{self.error_name}: {self.details}\n'
        return result

class Incorrect(Error):
    def __init__(self, details):
        super().__init__( 'Incorrect Character', details)

#Token Types 
TokenType_Int		= 'Int'
TokenType_Float    = 'Float'
TokenType_Plus     = 'Plus'
TokenType_Minus    = 'Minus'
TokenType_Multiply      = 'Multiply'
TokenType_Divide      = 'Divide'
TokenType_LeftParen   = 'LeftParen'
TokenType_RightParen   = 'RightParen'
TokenType_Mod      = 'MOD'
TokenType_Less      = 'Less'
TokenType_Great     = 'Great'
TokenType_LessEqual   = 'LessEqual'
TokenType_GreatEqual    = 'GreatEqual'
TokenType_Equal     = 'Equal'
TokenType_NotEqual   = 'NotEqual'

#type is the token type and value is the value under the type identified 
class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
#method used to make the print statement with type of token and the value it is
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#lexer class goes through each char to see what token type it is 
class Lexical:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

#goes to the next character in the text and if there is not another char then it wont run
    def advance(self):
        self.pos +=1
        self.current_char = self.text[self.pos] if self.pos < len(self.text)  else None

#start with an empty list for the tokens 
    def make_tokens(self):
        tokens = []
#while loop that goes through each char and see if it matches an on these char 
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in digi:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TokenType_Plus))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TokenType_Minus))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TokenType_Multiply))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TokenType_Divide))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType_LeftParen))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType_RightParen))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TokenType_Mod))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(TokenType_Less))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(TokenType_Great))
                self.advance()
            elif self.current_char == '<=':
                tokens.append(Token(TokenType_LessEqual))
                self.advance()
            elif self.current_char == '>=':
                tokens.append(Token(TokenType_GreatEqual))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(TokenType_Equal))
                self.advance()
            elif self.current_char == '!=':
                tokens.append(Token(TokenType_NotEqual))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], Incorrect( char )

        return tokens, None

    def make_number(self):
        num_str = ''
        decimal = 0


#checking if number is float or int only if the current character is not a none and the current character has the digits from above which is 0-9
        while self.current_char != None and self.current_char in digi + '.':
            if self.current_char == '.':
                if decimal == 1: break
                decimal += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if decimal == 0:
            return Token(TokenType_Int, int(num_str))
        else:
            return Token(TokenType_Float, float(num_str))


def start(text):
    lexer = Lexical(text)
    tokens, error = lexer.make_tokens()

    return tokens, error