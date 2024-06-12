from random import choice


def tictactoe_select(grid, selection, available_cells, item):
    result = False
    if selection > 8 or selection < 0:
        print("Invalid cell index. Please choose valid cell index from 0-8.")
    else:
        if grid[selection//3][selection % 3] == "-":
            grid[selection//3][selection % 3] = item
            available_cells.remove(selection)
            result = True
        else:
            print("Cell is already occupied, choose another cell.")
        for row in grid:
            for col in row:
                print(col, end=" ")
            print("")
    return result


def tictactoe_win(grid, item):
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] == item:
            return True

    for j in range(3):
        if grid[0][j] == grid[1][j] == grid[2][j] == item:
            return True

    if grid[0][0] == grid[1][1] == grid[2][2] == item:
        return True

    if grid[2][0] == grid[1][1] == grid[0][2] == item:
        return True

    return False


def tictactoe_main():
    grid = [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"],
    ]
    available_cells = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    print("Let's play tic-tac-toe! The cell indices are as shown:")
    print('''
        0 1 2
        3 4 5
        6 7 8
    ''')
    print("You are X, I will be O! You go first.")
    while True:
        try:
            selection = int(input("Enter cell index from 0-8 : "))
            if tictactoe_select(grid, selection, available_cells, "X"):
                if tictactoe_win(grid, "X"):
                    print("You win!")
                    decide = input("Enter y to play again : ").lower()
                    if decide == "y":
                        tictactoe_main()
                        break
                    else:
                        break
                if available_cells:
                    print("I will play this!")
                    tictactoe_select(grid, choice(available_cells), available_cells, "O")
                    if tictactoe_win(grid, "O"):
                        print("I win!")
                        decide = input("Enter y to play again : ").lower()
                        if decide == "y":
                            tictactoe_main()
                            break
                        else:
                            break
                else:
                    print("No more cells available, the game is a tie!")
                    decide = input("Enter y to play again : ").lower()
                    if decide == "y":
                        tictactoe_main()
                        break
                    else:
                        break
            else:
                continue
        except ValueError as err:
            print(err)


tictactoe_main()
