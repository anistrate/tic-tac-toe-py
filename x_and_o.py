
import platform
print(platform.python_version())

matrix  = []
matrix_size:int = 0
currentPlayer:int = 0
cellCoordinates = {
    "line" : -1,
    "column" : -1
    }
consecutive_cells_to_win:int = 5

def print_matrix():
    top_line:str = "      "
    top_separator_line:str  ="      "
    for i in range(0,matrix_size):
        top_line += str(i) + (" " if i>9 else "  ")
        top_separator_line += "-  "
    print(top_line)
    print(top_separator_line)
    for index, x in enumerate(matrix):
        line = get_line_character(index) + " " + "|" + "   "
        for y in x:
            line+= str(y) + "  "
        print(line)


def get_line_character(index:int) -> str:
   if index < 26:
        return chr(ord('a')+index)
   else:
       return chr(ord('A')+ index - 26)


def mark_cell(line:int,column:int, symbol:str):
    matrix[line][column] = symbol


def get_symbol_for_current_player() -> str:
    return "x" if currentPlayer == 1 else "o"


def change_player():
    global currentPlayer
    currentPlayer = 2 if currentPlayer == 1 else 1


def get_number_from_line_character(character:str) -> int:
    if ord(character) > 96 and ord(character) < 123:
       return ord(character) - 97
    elif ord(character) > 64 and ord(character) < 91:
        return ord(character) - 64 + 25
    else:
        raise Exception("Please insert a valid line number")

def cell_is_available(line:int, column:int) -> bool:
    return matrix[line][column] == '.'

def get_current_player_name() -> str:
    return player1 if currentPlayer == 1 else player2

def verify_if_player_won(line:int, column:int, symbol:str)-> bool:
    bottom_line = line-4 if line >= 4 else 0
    upper_line = line+5 if line+5 <= matrix_size else matrix_size

    bottom_column = column-4 if column >= 4 else 0
    upper_column = column+5 if column+5 <= matrix_size else matrix_size

    consecutive_cells = 0
    for i in range(bottom_line, upper_line):
        if matrix[i][column] == symbol:
            consecutive_cells+=1
        else:
            consecutive_cells = 0
        if consecutive_cells == consecutive_cells_to_win:
            sreturn True

    consecutive_cells = 0
    for j in range(bottom_column, upper_column):
        if matrix[line][j] == symbol:
            consecutive_cells+=1
        else:
            consecutive_cells = 0
        if consecutive_cells == consecutive_cells_to_win:
            return True

    consecutive_cells = 0
    for i in range(-4,5):
        if line + i >= 0 and column + i >= 0 and line + i < matrix_size and column + i < matrix_size:
            matrix[line+i][column+i] = 'x'
            if matrix[line+i][column+i] == symbol:
                consecutive_cells+=1
            else:
                consecutive_cells = 0
            if consecutive_cells == consecutive_cells_to_win:
                return True
            
    consecutive_cells = 0
    for i in range(-4,5):
        if line + i >= 0 and column - i >= 0 and line + i < matrix_size and column - i < matrix_size:
            if matrix[line+i][column-i] == symbol:
                consecutive_cells+=1
            else:
                consecutive_cells = 0
            if consecutive_cells == consecutive_cells_to_win:
                return True

    return False

player1:str = "Doge"
player2:str = "YunYun"
while True:
    try:
        print("Select the matrix size (min 5, max 51)")
        matrix_size = int(input(">"))
        if matrix_size < 5 or matrix_size > 51:
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
matrix = [['.' for x in range(matrix_size)] for y in range(matrix_size)]
someone_won:bool = False
board_was_chaged:bool = True

while not someone_won:
    try:
        if board_was_chaged == True:
            print_matrix()
        print(get_current_player_name() + "'s turn.")
        print("Insert " + get_symbol_for_current_player() + " at position: [a-Z] [0-52], eg v 20")
        cell_to_add = input(">")
        try:
            cells = cell_to_add.split(" ")
            if len(cells) != 2:
                raise Exception("Invalid format. Please insert in the valid format.")
            cellCoordinates["line"] = get_number_from_line_character(cells[0])
            cellCoordinates["column"] = int(cells[1])
            if cellCoordinates["line"] > matrix_size or cellCoordinates["line"] < 0:
                raise Exception("Invalid line symbol. Please insert a line number smaller than " + get_line_character(matrix_size))
            if cellCoordinates["column"] > matrix_size or cellCoordinates["column"] < 0:
                raise Exception("Invalid column symbol. Please insert a column number smaller than " + str(matrix_size))
            print(cellCoordinates)
            if cell_is_available(cellCoordinates["line"], cellCoordinates["column"]):
                mark_cell(cellCoordinates["line"], cellCoordinates["column"], get_symbol_for_current_player())
                if verify_if_player_won(cellCoordinates["line"], cellCoordinates["column"], get_symbol_for_current_player()):
                    someone_won = True
                else:
                    change_player()
                board_was_chaged = True
            else:
                print("That cell is already occupied. Please select a free cell.")
                board_was_chaged = False
        except ValueError:
            print("Error. Please insert a valid cell.")
            board_was_chaged = False
        except Exception as e:
            print(e)
            board_was_chaged = False
    except:
        print("Another error")
        board_was_chaged = False

print(get_current_player_name() + " won !!!")