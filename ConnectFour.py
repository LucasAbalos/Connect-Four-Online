import numpy
import pygame
import sys
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARE_SIZE = 100  # PIXELS

RADIUS = int(SQUARE_SIZE/2 - 5)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

pygame.init()

WIDTH = COLUMN_COUNT * SQUARE_SIZE
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE

SIZE = (WIDTH, HEIGHT)

SCREEN = pygame.display.set_mode(SIZE)


def creates_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))  # CREATES MATRIX OF 6 BY 7 FIGURES..(Y,X)
    return board


def drop_piece(board, row_, column, piece):
    board[row_][column] = piece


def is_valid_location(board, column):
    return board[ROW_COUNT - 1][column] == 0


def get_next_open_row(board, column):
    for row_ in range(ROW_COUNT):
        if board[row_][column] == 0:
            return row_


def print_board(board):
    print(numpy.flip(board, 0))  # THIS FLIPS THE BOARD SO THE (0,0) OF THE MATRIX IS ON THE BOTTOM


def winning_move(board, piece):
    correct = 0

    # CHECKS HORIZONTAL LOCATIONS FOR WIN
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                # print('HH board[{}][{}]'.format(r, c))
                correct += 1
                # print("HH Correct = ", correct)
            else:
                correct = 0
            if correct == 4:
                return True

    # CHECKS VERTICAL LOCATIONS FOR WIN
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == piece:
                # print('VV board[{}][{}]'.format(r, c))
                correct += 1
                # print("VV Correct = ", correct)
            else:
                correct = 0
            if correct == 4:
                return True

    # CHECKS DIAGONAL (UPWARDS - POSITIVES) LOCATIONS FOR WIN
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                print('UPWARD POSITIVE')
                return True

    # CHECKS DIAGONAL (UPWARDS - NEGATIVES) LOCATIONS FOR WIN
    for c in range(COLUMN_COUNT):
        if c >= 3:
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c - 1] == piece and board[r + 2][c - 2] == piece and board[r + 3][c - 3] == piece:
                    print('UPWARD NEGATIVE')
                    return True

    # CHECKS DIAGONAL (DOWNWARDS - POSITIVES ) LOCATIONS FOR WIN
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if r >= 3:
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    print('DOWNWARD POSITIVE')
                    return True

    # CHECKS DIAGONAL (DOWNWARDS - NEGATIVES) LOCATIONS FOR WIN
    for c in range(COLUMN_COUNT):
        if c >= 3:
            for r in range(ROW_COUNT):
                if r >= 3:
                    if board[r][c] == piece and board[r - 1][c - 1] == piece and board[r - 2][c - 2] == piece and board[r - 3][c - 3] == piece:
                        print('DOWNWARD NEGATIVE')
                        return True

    return False


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(SCREEN, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(SCREEN, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE/2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(SCREEN, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            elif board[r][c] == 2:
                pygame.draw.circle(SCREEN, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    pygame.display.update()


def main():
    board_1 = creates_board()  # INITIALIZE BOARD, CREATES ONE
    print_board(board_1)
    turn = 1

    game_over = False

    draw_board(board_1)

    my_font = pygame.font.SysFont("monospace", 40)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn == 1:
                    pygame.draw.circle(SCREEN, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
                if turn == 2:
                    pygame.draw.circle(SCREEN, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0, 0, WIDTH, SQUARE_SIZE))

                col = 10  # THIS IS A PREDEFINE TO AVOID ERRORS

                if turn == 1:  # ASK FOR PLAYER 1 INPUT
                    while col >= 7 or col < 0:
                        pos_x = event.pos[0]
                        col = int(math.floor(pos_x/SQUARE_SIZE))
                if turn == 2:  # ASK FOR PLAYER 2 INPUT
                    while col >= 7 or col < 0:
                        pos_x = event.pos[0]
                        col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board_1, col):
                    row = get_next_open_row(board_1, col)
                    drop_piece(board_1, row, col, turn)

                if winning_move(board_1, turn):
                    label = my_font.render('Congrats Player {}, you won!!'.format(turn), True, GREEN)
                    SCREEN.blit(label, (15, 10))
                    game_over = True

                print_board(board_1)
                draw_board(board_1)

                turn = turn % 2  # THE FOLLOWING 2 LINES LOOPS BTW PLAY1 AN PLAY2
                turn = turn + 1

                if game_over:
                    pygame.time.wait(3000)
                    quit()


if __name__ == '__main__':
    main()
