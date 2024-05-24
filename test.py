import pygame as pg
import sys
import time
import random
from sudoku import SudokuCreator
import copy
pg.init()
screen_size =750,800
screen =pg.display.set_mode(screen_size)
font =pg.font.SysFont(None,80)
game = SudokuCreator()


def remove_numbers(board, num=30):
    removed = 0
    while removed < num:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if board[row][col] != 0:  # Ensure we don't select an already empty cell
            backup = board[row][col]
            board[row][col] = 0
            # Use a backtracking algorithm to count the solutions
            solutions = count_solutions(board)
            if solutions == 1:  # If there is a unique solution
                removed += 1
            else:  # If there is more than one solution
                board[row][col] = backup  # Put the number back
    return board

def count_solutions(board, row=0, col=0):
    if row == 9:  # If we have filled all cells
        return 1
    if col == 9:  # If we have filled all cells in the current row
        return count_solutions(board, row + 1, 0)
    if board[row][col] != 0:  # If the current cell is not empty
        return count_solutions(board, row, col + 1)
    count = 0
    for num in range(1, 10):  # Try all possible numbers
        if is_valid(board, row, col, num):  # If the number is valid
            board[row][col] = num
            count += count_solutions(board, row, col + 1)
            board[row][col] = 0
    return count

def is_valid(board, row, col, num):
    # Check the row
    for x in range(9):
        if board[row][x] == num:
            return False
    # Check the column
    for x in range(9):
        if board[x][col] == num:
            return False
    # Check the box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

start_time = pg.time.get_ticks()
full_board=game.create_puzzle()
user_numbers = [[0 for _ in range(9)] for _ in range(9)]  # Keep track of the numbers added by the user
board = remove_numbers(copy.deepcopy(full_board))
for i in range(9):
    for j in range(9):
        print(full_board[i][j], end=' ')
    print()
selected_square = None

def draw_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    if selected_square:  # If a square is selected
        pg.draw.rect(screen, pg.Color("red"), pg.Rect(selected_square[0]*80+15, selected_square[1]*80+15, 80, 80), 8)  # Draw a rectangle around the selected square
    i =1
    while (i * 80) < 720:
        line_width =5 if i%3 >0 else 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), line_width)
        i += 1
mistakes =0

def game_loop():
    global selected_square, mistakes
    game_over =False
    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Mouse click event
                mouse_pos = pg.mouse.get_pos()
                selected_square = mouse_pos[0] // 80, mouse_pos[1] // 80  # Get the clicked square
            elif event.type == pg.KEYDOWN:# Key press event
                if event.key in (pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT):  # If an arrow key is pressed
                    if selected_square:  # If a square is selected
                        if event.key == pg.K_UP and selected_square[1] > 0:  # If the up arrow key is pressed and the selected square is not in the top row
                            selected_square = selected_square[0], selected_square[1] - 1  # Move the selection up
                        elif event.key == pg.K_DOWN and selected_square[1] < 8:  # If the down arrow key is pressed and the selected square is not in the bottom row
                            selected_square = selected_square[0], selected_square[1] + 1  # Move the selection down
                        elif event.key == pg.K_LEFT and selected_square[0] > 0:  # If the left arrow key is pressed and the selected square is not in the leftmost column
                            selected_square = selected_square[0] - 1, selected_square[1]  # Move the selection left
                        elif event.key == pg.K_RIGHT and selected_square[0] < 8:  # If the right arrow key is pressed and the selected square is not in the rightmost column
                            selected_square = selected_square[0] + 1, selected_square[1]  # Move the selection right
                if selected_square:  # If a square is selected
                    if board[selected_square[1]][selected_square[0]] == 0:  # If the square is empty
                        if event.unicode.isdigit() and 0 < int(event.unicode) < 10:  # If the key is a number between 1 and 9
                            board[selected_square[1]][selected_square[0]] = int(event.unicode)  # Update the board
                            user_numbers[selected_square[1]][selected_square[0]] = 1  # Mark the number as added by the user
                    elif user_numbers[selected_square[1]][selected_square[0]]:  # If the square contains a number added by the user
                        if event.key == pg.K_BACKSPACE:  # If the backspace key is pressed
                            if user_numbers[selected_square[1]][selected_square[0]] != 2:  # If the number is not marked as correct
                                board[selected_square[1]][selected_square[0]] = 0  # Delete the number
                                user_numbers[selected_square[1]][selected_square[0]] = 0  # Unmark the number as added by the user
                        elif event.key == pg.K_RETURN:  # If the enter key is pressed
        # Your existing code...
                            if board[selected_square[1]][selected_square[0]] == full_board[selected_square[1]][selected_square[0]]:  # If the entered number is correct
                                user_numbers[selected_square[1]][selected_square[0]] = 2  # Mark the number as correct
                            else:  # If the entered number is incorrect
                                user_numbers[selected_square[1]][selected_square[0]] = 3  # Mark the number as incorrect
                                mistakes += 1  # Increment the mistakes counter

        # Check if the board is complete
        # Check if the board is complete
        if board == full_board:
            print(f'Congratulations! You completed the board with {mistakes} mistakes.')
            game_over=True

        draw_background()
        draw_numbers()
        pg.display.flip()
        if game_over:
                # Create a font object
                font = pg.font.Font(None, 36)

                # Render the text
                text = font.render(f'Congratulations! You completed the board with {mistakes} mistakes.', True, (0, 0, 0))

                # Get the width and height of the text surface
                text_width = text.get_width()
                text_height = text.get_height()

                # Calculate the position to center the text
                pos_x = (800 - text_width) // 2
                pos_y = (800 - text_height) // 2

                # Blit the text onto the screen
                screen.blit(text, (pos_x, pos_y))
                s = pg.Surface((800,800))  # the size of your screen
                s.set_alpha(128)  # alpha level
                s.fill((255,255,255))  # this fills the entire surface
                screen.blit(s, (0,0))  # (0,0) are the top-left coordinates
                pg.display.flip()

                while True:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()

def draw_numbers():
    row = 0
    offset = 40
    while row < 9:
        col = 0
        while col < 9:
            output = board[row][col]
            if output == 0:
                n_text = font.render(str(" "), True, pg.Color('white'))
                screen.blit(n_text, pg.Vector2((col * 80) + offset, (row * 80) + offset))
            else:
                color = pg.Color('green') if user_numbers[row][col] == 2 else pg.Color('red') if user_numbers[row][col] == 3 else pg.Color('blue') if user_numbers[row][col] == 1 else pg.Color('black')
                n_text = font.render(str(output), True, color)
                screen.blit(n_text, pg.Vector2((col * 80) + offset, (row * 80) + offset))
            col += 1
        row += 1

    # Draw the mistakes counter
    mistakes_text = font.render(f'Mistakes: {mistakes}', True, pg.Color('black'))
    screen.blit(mistakes_text, pg.Vector2(10, screen_size[1] - mistakes_text.get_height() - 10))  # Adjust the position as needed
        # Draw the timer
    elapsed_time = pg.time.get_ticks() - start_time
    minutes = elapsed_time // 60000  # Convert milliseconds to minutes
    seconds = (elapsed_time // 1000) % 60  # Convert milliseconds to seconds

    # Create a surface with the time
    timer_surface = font.render(f'{minutes}:{seconds:02}', True, pg.Color('black'))

    # Draw the timer on the screen
    screen.blit(timer_surface, (screen_size[0] - timer_surface.get_width() - 10, screen_size[1] - timer_surface.get_height() - 10))


while 1:
    game_loop()