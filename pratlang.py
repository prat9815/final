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

#making a node class that takes in an integer or a float token 
class Node: 
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'
# class for the binary operation showing the left and right node and the operator in betweeen(+,-,*,/)      
class BinaryOp:
    def __init__(self, left_node,operator, right_node):
        self.left_node = left_node
        self.operator = operator
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.operator}, {self.right_node})'
#the parser takes the first token in the expression and advance through the whole expression
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()
#advance function allows to move onto the next token in the expression     
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.present_token = self.tokens[self.token_index]
        return self.present_token
#    
    def parsing(self):
        value = self.expression()
        return value
#making a factor class that is either a integer or a float and if it is one of them then it advances to next token   
#factor : int or float
    def factor(self): 
        tok = self.present_token
        if tok.type in (TokenType_Int, TokenType_Float):
            self.advance()
        return Node(tok)
        
#expression in my language is a plus or a minus
#expression = term + or - term
    def expression(self):
        left = self.term()
        while self.present_token.type in (TokenType_Plus, TokenType_Minus):
            operator = self.present_token
            self.advance()
            right = self.term()
            left = BinaryOp(left, operator, right)
        return left
        
#term in my language is multiply or divide
#term = factor * or / factor 
    def term(self):
        left = self.factor()
        while self.present_token.type in (TokenType_Multiply, TokenType_Divide):
            operator = self.present_token
            self.advance()
            right = self.factor()
            left = BinaryOp(left, operator, right)
        return left
        






def start(text):
    lexer = Lexical(text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    p = Parser(tokens)
    tree = p.parsing()

    return tree, None