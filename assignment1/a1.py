# CMPUT 455 Assignment 1 
# Jake Frenette, Student Number: 1426995, CCID: jlfrenet
# Implement the specified commands to complete the assignment
# Full assignment specification and game rules on Canvas
 
from sys import stderr
from typing import List, Dict, Callable
import random
#from GameBoard import Token, Stack, GameBoard

numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# Use randy to generate random integers in range[start, stop+1] with step of 1 
# Optional seed argument for testing and debugging. Seed default is None.
def randy(stop, start=1, seed=None) -> int:
    if seed is not None:
        random.seed(seed)
    return random.randrange(start, stop+1)

def not_yet() -> bool:
    raise NotImplementedError("Command not implemented.")
    return False

def print_error(error: str) -> None:
    print(error, file = stderr)

CommandMap = Dict[str, Callable[[str], bool]]

class CommandInterface:
    def __init__(self) -> None:
        # you can add your own initialisation here
        self.game = None
        self.board = None
        self.komi = None
        self.player1 = None
        self.player2 = None
        self.commands: CommandMap = {
            "help": self.cmd_help,
            "heapgo": self.cmd_heapgo,
            "show": self.cmd_show,
            "toplay": self.cmd_toplay,
            "play": self.cmd_play,
            "legal": self.cmd_legal,
            "genmove": self.cmd_genmove,
            "score": self.cmd_score,
            "winner": self.cmd_winner,
            }

#============================================================================
# You need to implement the following methods.
#============================================================================
    def cmd_heapgo(self, args: str) -> bool:
        '''
        This function is called when the command heapgo is given, it creates a 
        new game of heap go.
        Arguments:
            + Self: this function must be called on an object of the CommandInterface class
            + args: a string object to be parsed inside this function.
                    args must contain the following information in precisely this format:
                    "komi GameString" . Komi represents a float number. A decimal should be given.
                    GameString is a nested list containing game tokens. Each of the nested lists
                    represent a heap of the heapgo board. The tokens are the tokens contained in
                    each respective heap. 
        Returns:
            + status: A bool value representing whether the heapgo command ran succesfully (True) or not (False) 
        '''
        # Evaluate arguments input. Require komi (float) and game string.
        # Every other type of input should give error
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']
        status = False
        args =args.strip()
        arguments = args.split(maxsplit=1)
        # arguments[0] should be komi, arguments[1] should be gamestring
        # verify komi is valid
        for chara in arguments[0]:
            if chara not in numbers:
                return status
        self.komi = float(arguments[0])
        gamestr = arguments[1].strip()
        # Evaluate GameString input
        length = len(gamestr)
        if gamestr[0] != "[" or gamestr[length -1] != "]":
            return status
        gameboard = []
        new_heap = None
        new_token = False
        for symbol in range(1, length-1):
            if gamestr[symbol] == "[":
                new_heap = []
            if gamestr[symbol] == "]":
                gameboard.append(new_heap)
            if gamestr[symbol] == "(":
                new_token = self.process_token(gamestr, symbol)
                if type(new_token)==bool and new_token==False:
                    return status
                else:
                    new_heap.append(new_token)
        # By here, the gameboard should be ready to make
        if len(gameboard) > 0:
            self.board = GameBoard(gameboard=gameboard)
        if self.board is not None:
            self.game = HeapGo(self.board, self.komi)
            status = True
            
        return status
    
    def cmd_show(self, args: str) -> bool:
        status = False
        if self.komi is not None and self.board is not None:
            print(f"k {self.komi} {self.board.print_it()}")
            status = True
        return status
    
    def cmd_toplay(self, args: str) -> bool:
        status = False
        args = args.strip()
        parts = args.split(maxsplit=1)
        if len(parts[0]) == 1:
            player = parts[0]
            if ascii(player) == ascii("b") or ascii(player) == ascii("w"):
                self.game.set_to_play(player)
                status = True
            
        return status
        
    def cmd_play(self, args: str) -> bool:
        status = False
        args = args.strip()
        parts = args.split(maxsplit=1)
        if len(parts[0]) == 1:
            if parts[0] in numbers:
                num = int(parts[0])
                if self.game.is_legal(num): 
                    self.game.play_move(num)
                    status = True
                           
        return status
    
    def cmd_legal(self, args: str) -> bool:
        status = False
        args = args.strip()
        parts = args.split(maxsplit=1)
        if len(parts[0]) == 1:
            if parts[0] in numbers:
                num = int(parts[0])
                if self.game.is_legal(num):
                    print("yes")
                else:
                    print("no")
                status = True
        
        return status
    
    def cmd_genmove(self, args: str) -> bool:
        status = False
        legal_moves = self.game.legal_moves()
        if len(legal_moves) > 0:
            rand = randy(len(legal_moves)) - 1
            self.game.play_move(legal_moves[rand])
            print(legal_moves[rand])
            status = True
        return status
    
    def cmd_score(self, args: str) -> bool:
        status = False
        score = self.game.get_score()
        print(f"b {score[1]} w {score[3]}")
        status = True
        return status
    
    def cmd_winner(self, args: str) -> bool:
        status = False
        if self.game.is_over():
            
            score = self.game.get_score()
            tot = score[1] - score[3]
            if tot > 0:
                print("b")
                status = True
            elif tot < 0:
                print("w")
                status = True
                
        return status
#============================================================================
# End of functions requiring implementation
#============================================================================

#============================================================================
# The code below should not need modification
# Anyway, you may change or add to this code as you see fit
# Examples:
# You can add class variables to __init__ above
# You can add better error messages
# You can put commands inside your own Heap Go class
# etc.
#============================================================================
    # List available commands
    def cmd_help(self, ignore_args: str) -> bool:
        print("\nKnown commands:")
        for cmd in self.commands:
            print(cmd)
        return True

    def process_command(self, cmd_name: str, cmd_args: str) -> None:
        # Try to find command, None if wrong name
        status = "= -1"
        cmd = self.commands.get(cmd_name)
        if cmd:
            try:
                if cmd(cmd_args): # success!
                    status = "= 1"
            except Exception as e:
                print_error(f"Command {cmd_name} with arguments {cmd_args} failed with exception: {e}")
        else:
            print_error("Unknown command. Type 'help' for commands.")
        print(status)
    
    def main_loop(self) -> None:
        process_commands = True
        while process_commands:
            try:
                line = input()
            except EOFError:
                break
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            cmd_name = parts[0]
            if cmd_name == "exit":
                process_commands = False
                continue
            cmd_args = parts[1] if len(parts) > 1 else ""
            self.process_command(cmd_name, cmd_args)
            
            
    def process_token(self, gamestring, index):
        token = False
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        length = len(gamestring)
        if index >= length-1:
            return token
        letter = None  # where we put the token's color designator
        close_apos = 0  # turns to 1 if you have encountered an open apostrophy and are waiting to encounter a close apostrophy
        two_dig = False  # becomes true if a token's value is a two digit number
        val = None   # where we put the token's value
        for i in range(index+1, length-1):
            if gamestring[i] == "'" and close_apos == 0:
                close_apos = 1
                
                if (ascii(gamestring[i+1]) == ascii("b")) or (ascii(gamestring[i+1]) == ascii("w")):
                    letter = gamestring[i+1]
            if gamestring[i] == "'" and close_apos == 1:
                close_apos = 0
            if gamestring[i] == " " and close_apos == 1:
                return False
            if gamestring[i] in numbers:
                if gamestring[i+1] in numbers:
                    two_dig = True
                    valinterm = int(gamestring[i:i+2])
                    val = int(valinterm)
                elif not two_dig:
                    val = int(gamestring[i])
                    two_dig = False    
            if gamestring[i] == ")":
                if letter is None:
                    return token
                token = (letter, val)
                two_dig = False  
                return token  
        return token
    
    
class HeapGo:
    def __init__(self, gameboard, komi):
        self.gameboard = gameboard
        self.komi = komi
        self.black = None
        self.white = None
        self.to_play = "b"
        self.score = {"b": 0, "w": self.komi}
        self.over = False
        
    def get_to_play(self):
        return self.to_play
    
    def set_to_play(self, play_str)->bool:
        status = False
        if len(play_str) != 1:
            return status
        if ascii(play_str) == ascii("b") or ascii(play_str) == ascii("w"):
            self.to_play = play_str
            status = True
        return status
    
    def add_point(self, value)->bool:
        status = False
        if type(value) == int:
            self.score[self.get_to_play()] += value
            status = True
        return status
    
    def get_score(self):
        return ("b", self.score["b"], "w", self.score["w"])

    def is_legal(self, heap_num)->bool:
        answer = False
        if heap_num <= self.gameboard.get_number_heaps()-1:
            if not self.gameboard.get_heap(heap_num).is_empty():
                answer = True
        return answer
    
    def legal_moves(self)->list:
        # returns the heap numbers of where it is legal to play
        legal_moves = []
        for hep in range(0, self.gameboard.get_number_heaps()):
            if self.is_legal(hep):
                legal_moves.append(hep)
        return legal_moves
    
    def is_over(self)->bool:
        over = False
        if len(self.legal_moves()) == 0:
            over = True
        return over
        
    def play_move(self, heap_num)->bool:
        status = False
        if self.is_legal(heap_num):
            toke = self.gameboard.get_heap(heap_num).pop()
            self.add_point(toke.get_value())
            if ascii(self.get_to_play()) == ascii(toke.get_colour()):
                popping = True
                while popping and not self.gameboard.get_heap(heap_num).is_empty():
                    toke = self.gameboard.get_heap(heap_num).pop()
                    self.add_point(toke.get_value())
                    if ascii(self.get_to_play()) != ascii(toke.get_colour()):
                        popping = False
                
            # switch to other player's turn
            if ascii(self.get_to_play()) == ascii("b"):
                self.set_to_play("w")
            else:
                self.set_to_play("b")
            status = True
            
        return status 
    
    
# Use randy to generate random integers in range[start, stop+1] with step of 1 
# Optional seed argument for testing and debugging. Seed default is None.
class Randy:
    def __init__(self, seed=None) -> None:
        self._seed = seed
        
    def get_randy(self, stop, start=1):
        random.seed(self._seed)
        return random.randrange(start, stop+1)

class Token:
# Token class creates an instance of a token object, a tuple containing a colour
# either 'b' for black or 'w' for white, and a value between 1 and 20 inclusive.
# The colour and value are randomly chosen using the randy function. Once testing 
# is done, make sure to remove the seed=2 from the calls to randy.    
    def __init__(self, tup=None) -> None:
        if tup is None:
            # make new random token
            randal1 = Randy()
            randal2 = Randy()
            self._value = int(randal1.get_randy(20, start=0) ) # remove seed after testing
            colour = randal2.get_randy(2)  # remove seed after testing
            if colour == 1:
                self._colour = "b"
            else:
                self._colour = "w"
        else:
            self._colour = tup[0]
            self._value = tup[1]
                
        self._token = (self._colour, self._value)
    
    def get_token(self) -> tuple:
        return self._token
    
    def get_value(self) -> int:
        return self._value
    
    def get_colour(self) -> str:
        return self._colour

    def __str__(self) -> str:
        if self.get_value() < 10:   
            token_string = f"({self.get_colour()},  {self.get_value()})"
        else:
            token_string = f"({self.get_colour()}, {self.get_value()})"
            
        return token_string

class Stack:
    
    def __init__(self) -> None:
        
        self._stack = []
        self._size = 0
        
    def push(self, obj) -> None:
        # This method takes a Token object (obj) as an argument and pushes it to
        # the top of the stack
        self._stack.append(obj)
        self._size += 1
        
    def pop(self) -> Token:
        # This method pops the top item from a stack and returns it
        if not self.is_empty():
            obj = self._stack[self._size - 1]
            self._stack.pop(self._size - 1)
            self._size -= 1
            return obj
        else:
            print("Woops, stack is already empty.")
            return None

    def size(self) -> int:
        # This method returns the current number of Tokens in the stack
        return self._size
    
    def peek(self) -> Token: 
        # returns the top-most element in the stack without removing it 
        # from the stack
        top = self.size() -1
        return self._stack[top]
    
    def is_empty(self) -> bool:
        # returns True if stack is empty, False otherwise.
        empty = False
        if (self.size() == 0):
            empty = True
        
        return empty
    
    def state(self) -> list:
        # This method returns the current stack so it can be viewed
        # or printed
        return self._stack
    
    def __str__(self) -> str:
        final_string = f"+---------+\n"
        the_stack = self.state()
        for token in the_stack:
            token_string = f"| {token.__str__()} | \n"
            final_string = token_string + final_string
            
        return final_string

class GameBoard:
    def __init__(self, gameboard=None, number_heaps=0) -> None:
        self.board = []
        if gameboard is not None:
            self.number_heaps = len(gameboard)
           
            for heap in gameboard:
                hep = Stack()
                for token in heap:
                    # make token with color and value of that in gameboard[heap]
                    toke = Token(token)
                    hep.push(toke)
                self.board.append(hep)
                    
        else:
            if number_heaps == 0:
                # generate random number of heaps between 1 and 10
                randal1 = Randy()
                number_heaps = randal1.get_randy(10)
            
            if (number_heaps < 0) or (number_heaps > 10):
                print("Error. The number of heaps must be between 1 and 10.")
        
            self.number_heaps = number_heaps    
               
            for heap in range(0, self.number_heaps):
                h = Stack()
            
                # generate a random number of tokens for the stack between 1 and 10
                randal2 = Randy()
                num_tokens = randal2.get_randy(10)
                for toke in range(0, num_tokens):
                    t = Token()
                    h.push(t)
                self.board.append(h)
    
    def get_number_heaps(self) -> int:
        return self.number_heaps
    
    def get_heap(self, heap_index) -> Stack:
        # make sure heap_index is a valid number between 0 and self.number_heaps
        if (heap_index < 0) or (heap_index > self.get_number_heaps()):
            print(f"Error. Please enter a heap number between 0 and {self.get_number_heaps}")
        
        return self.board[heap_index]
    
    def __str__(self) -> str:
        print("\n")
        line0 = f""
        line1 = f""
        line2 = f""
        line3 = f""
        line4 = f""
        line5 = f""
        line6 = f""
        line7 = f""
        line8 = f""
        line9 = f""
        line10 = f""
        line11 = f""
        
        line_list = [line0,
                     line1,
                     line2,
                     line3,
                     line4,
                     line5,
                     line6,
                     line7,
                     line8,
                     line9,
                     line10,
                     line11]
        
        for heap in range(0, self.number_heaps):
            line_list[11] = line_list[11] + f"     {heap}      "
            line_list[10] = line_list[10] + f"+---------+ "
            the_heap = self.board[heap].state()
            height = len(the_heap)
            
            for token in range(0, height):
                line_list[9 - token] = line_list[9 - token] + f"| {the_heap[token].__str__()} | "
                
            for empty in range(height, 10):
                line_list[9 - empty] = line_list[9 - empty] + f"|         | "
        final_str = ""
        for line in line_list:
            line = line + "\n"
            final_str = final_str + line
        
        final_str = final_str + "\n"
            
        return final_str
    def print_it(self):
        as_lst = []
        for h in range(0, self.get_number_heaps()):
            as_lst.append([])
            hep = self.get_heap(h)
            for tok in range(0, hep.size()):
                as_lst[h].append(hep.state()[tok].get_token())
        return as_lst


       
if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()

