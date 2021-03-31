import json
import sys

class Game:
    def __init__(self, data:json):
       self.matrix_size:int = data['matrix_size']
       self.player1:str = data['first_player']
       self.player2:str = data['second_player']
       self.port:int = data['port']
       self.currentPlayer:int = data['player_starting_first']
       self.matrix:list = [['.' for x in range(self.matrix_size)] for y in range(self.matrix_size)]
       self.cellCoordinates:dict = {"line" : -1, "column" : -1 }
       self.consecutive_cells_to_win:int = 5
       self.someone_won:bool = False
       self.board_was_chaged:bool = True

    def print_matrix(self):
        top_line:str = "      "
        top_separator_line:str  ="      "
        for i in range(0,self.matrix_size):
            top_line += str(i) + (" " if i>9 else "  ")
            top_separator_line += "-  "
        print(top_line)
        print(top_separator_line)
        for index, x in enumerate(self.matrix):
            line = self.get_line_character(index) + " " + "|" + "   "
            for y in x:
                line+= str(y) + "  "
            print(line)

    def get_line_character(self,index:int) -> str:
        if index < 26:
            return chr(ord('a')+index)
        else:
            return chr(ord('A')+ index - 26)

    def mark_cell_as_occupied(self, line:int,column:int, symbol:str):
        self.matrix[line][column] = symbol
    
    def get_symbol_for_current_player(self) -> str:
        return "x" if self.currentPlayer == 1 else "o"

    def change_current_player(self):
        self.currentPlayer = 2 if currentPlayer == 1 else 1

    def get_number_from_line_character(self,character:str) -> int:
        if ord(character) > 96 and ord(character) < 123:
            return ord(character) - 97
        elif ord(character) > 64 and ord(character) < 91:
            return ord(character) - 64 + 25
        else:
            raise Exception("Please insert a valid line number")

    def cell_is_available(self,line:int, column:int) -> bool:
        return self.matrix[line][column] == '.'

    def get_current_player_name(self) -> str:
        return self.player1 if self.currentPlayer == 1 else self.player2

    def verify_if_player_won(self, line:int, column:int, symbol:str)-> bool:
        bottom_line = line-4 if line >= 4 else 0
        upper_line = line+5 if line+5 <= self.matrix_size else self.matrix_size

        bottom_column = column-4 if column >= 4 else 0
        upper_column = column+5 if column+5 <= self.matrix_size else self.matrix_size

        consecutive_cells = 0
        for i in range(bottom_line, upper_line):
            if self.matrix[i][column] == symbol:
                consecutive_cells+=1
            else:
                consecutive_cells = 0
            if consecutive_cells == self.consecutive_cells_to_win:
                return True

        consecutive_cells = 0
        for j in range(bottom_column, upper_column):
            if self.matrix[line][j] == symbol:
                consecutive_cells+=1
            else:
                consecutive_cells = 0
            if consecutive_cells == self.consecutive_cells_to_win:
                return True

        consecutive_cells = 0
        for i in range(-4,5):
            if line + i >= 0 and column + i >= 0 and line + i < self.matrix_size and column + i < self.matrix_size:
                if self.matrix[line+i][column+i] == symbol:
                    consecutive_cells+=1
                else:
                    consecutive_cells = 0
                if consecutive_cells == self.consecutive_cells_to_win:
                    return True
            
        consecutive_cells = 0
        for i in range(-4,5):
            if line + i >= 0 and column - i >= 0 and line + i < self.matrix_size and column - i < self.matrix_size:
                if self.matrix[line+i][column-i] == symbol:
                    consecutive_cells+=1
                else:
                    consecutive_cells = 0
                if consecutive_cells == self.consecutive_cells_to_win:
                    return True

        return False

    def run_game_loop(self):
        while not self.someone_won:
            try:
                if self.board_was_chaged == True:
                    self.print_matrix()
                print(self.get_current_player_name() + "'s turn.")
                print("Insert " + self.get_symbol_for_current_player() + " at position: [a-Z] [0-52], eg v 20")
                cell_to_add = input(">")
                try:
                    cells = cell_to_add.split(" ")
                    if len(cells) != 2:
                        raise Exception("Invalid format. Please insert in the valid format.")
                    self.cellCoordinates["line"] = self.get_number_from_line_character(cells[0])
                    self.cellCoordinates["column"] = int(cells[1])
                    if self.cellCoordinates["line"] > self.matrix_size or self.cellCoordinates["line"] < 0:
                        raise Exception("Invalid line symbol. Please insert a line number smaller than " + self.get_line_character(self.matrix_size))
                    if self.cellCoordinates["column"] > self.matrix_size or self.cellCoordinates["column"] < 0:
                        raise Exception("Invalid column symbol. Please insert a column number smaller than " + str(self.matrix_size))
                    print(self.cellCoordinates)
                    if self.cell_is_available(self.cellCoordinates["line"], self.cellCoordinates["column"]):
                        self.mark_cell_as_occupied(self.cellCoordinates["line"], self.cellCoordinates["column"], self.get_symbol_for_current_player())
                        if self.verify_if_player_won(self.cellCoordinates["line"], self.cellCoordinates["column"], self.get_symbol_for_current_player()):
                            self.someone_won = True
                        else:
                            self.change_player()
                        self.board_was_chaged = True
                    else:
                        print("That cell is already occupied. Please select a free cell.")
                        self.board_was_chaged = False
                except ValueError as e:
                    print(e)
                    print("Error. Please insert a valid cell.")
                    self.board_was_chaged = False
                except Exception as e:
                    print(e)
                    self.board_was_chaged = False
            except:
                print("Another error")
                self.board_was_chaged = False
    
    def display_winning_player(self):
        self.print_matrix()
        print(self.get_current_player_name() + " won !!!")
                        
def print_usage():
    print(f"usage: {sys.argv[0]} " +'{-in | -js -p path | -cmd -p1 player1 -p2 player2 -po port -ms matrix_size} [[-sp 1|2] | r ]')

def init_from_standard_input():
    while True:
        try:
            print("Select the matrix size (min 15, max 51)")
            matrix_size = int(input(">"))
            if matrix_size < 15 or matrix_size > 51:
                continue
            matrix_size+=1
            print("Which player starts first?")
            print("Doge - 1")
            print("YunYun - 2")
            currentPlayer = int(input(">"))
            if currentPlayer == 1 or currentPlayer == 2:
                break
            else:
                print("Please insert either 1 or 2")
                continue
            break
        except:
            print("Error. Please insert a number.")

print_usage()

with open("init_file.json") as json_file:
    data = json.load(json_file)

newGame = Game(data)
newGame.run_game_loop()
newGame.display_winning_player()

# while not someone_won:
#     try:
#         if board_was_chaged == True:
#             print_matrix()
#         print(get_current_player_name() + "'s turn.")
#         print("Insert " + get_symbol_for_current_player() + " at position: [a-Z] [0-52], eg v 20")
#         cell_to_add = input(">")
#         try:
#             cells = cell_to_add.split(" ")
#             if len(cells) != 2:
#                 raise Exception("Invalid format. Please insert in the valid format.")
#             cellCoordinates["line"] = get_number_from_line_character(cells[0])
#             cellCoordinates["column"] = int(cells[1])
#             if cellCoordinates["line"] > matrix_size or cellCoordinates["line"] < 0:
#                 raise Exception("Invalid line symbol. Please insert a line number smaller than " + get_line_character(matrix_size))
#             if cellCoordinates["column"] > matrix_size or cellCoordinates["column"] < 0:
#                 raise Exception("Invalid column symbol. Please insert a column number smaller than " + str(matrix_size))
#             print(cellCoordinates)
#             if cell_is_available(cellCoordinates["line"], cellCoordinates["column"]):
#                 mark_cell(cellCoordinates["line"], cellCoordinates["column"], get_symbol_for_current_player())
#                 if verify_if_player_won(cellCoordinates["line"], cellCoordinates["column"], get_symbol_for_current_player()):
#                     someone_won = True
#                 else:
#                     change_player()
#                 board_was_chaged = True
#             else:
#                 print("That cell is already occupied. Please select a free cell.")
#                 board_was_chaged = False
#         except ValueError:
#             print("Error. Please insert a valid cell.")
#             board_was_chaged = False
#         except Exception as e:
#             print(e)
#             board_was_chaged = False
#     except:
#         print("Another error")
#         board_was_chaged = False

# print_matrix()
# print(get_current_player_name() + " won !!!")