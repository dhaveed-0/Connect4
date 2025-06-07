import sys
import numpy as np
import pygame
import math

# ─────── Constants ─────────────────────────────────────────────────────────────

ROW_COUNT = 6
COL_COUNT = 7
SQUARESIZE = 100         # pixel size of each square
RADIUS = int(SQUARESIZE / 2 - 5)

# Colors (RGB)wo
BLUE   = (  0,   0, 255)
BLACK  = (  0,   0,   0)
RED    = (255,   0,   0)
YELLOW = (255, 255,   0)

# Screen dimensions
width  = COL_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE    # extra row at top for dropping piece preview
size   = (width, height)

# ─────── Board Logic ───────────────────────────────────────────────────────────

def create_board():
    """Return a 6×7 zero-filled NumPy array."""
    board = np.zeros((ROW_COUNT, COL_COUNT), dtype=int)
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return None

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c]     == piece and
                board[r][c + 1] == piece and
                board[r][c + 2] == piece and
                board[r][c + 3] == piece):
                return True

    # Check vertical locations for win
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c]     == piece and
                board[r + 1][c] == piece and
                board[r + 2][c] == piece and
                board[r + 3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c]       == piece and
                board[r + 1][c + 1] == piece and
                board[r + 2][c + 2] == piece and
                board[r + 3][c + 3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COL_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c]       == piece and
                board[r - 1][c + 1] == piece and
                board[r - 2][c + 2] == piece and
                board[r - 3][c + 3] == piece):
                return True

    return False

def is_board_full(board):
    return all(board[ROW_COUNT - 1][c] != 0 for c in range(COL_COUNT))

# ─────── Drawing ────────────────────────────────────────────────────────────────

def draw_board(board, screen):
    """Draw the entire board on the Pygame window."""
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            # Draw the blue square
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    c * SQUARESIZE,
                    (r + 1) * SQUARESIZE,
                    SQUARESIZE,
                    SQUARESIZE
                )
            )
            # Draw the empty circle (black hole) or piece
            if board[ROW_COUNT - 1 - r][c] == 0:
                pygame.draw.circle(
                    screen,
                    BLACK,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int((r + 1) * SQUARESIZE + SQUARESIZE / 2)
                    ),
                    RADIUS
                )
            elif board[ROW_COUNT - 1 - r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int((r + 1) * SQUARESIZE + SQUARESIZE / 2)
                    ),
                    RADIUS
                )
            else:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int((r + 1) * SQUARESIZE + SQUARESIZE / 2)
                    ),
                    RADIUS
                )
    pygame.display.update()

# ─────── Main Game Loop ─────────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4")

    board = create_board()
    draw_board(board, screen)
    pygame.display.update()

    font = pygame.font.SysFont("monospace", 75)
    game_over = False
    turn = 0   # 0: Player 1 (RED), 1: Player 2 (YELLOW)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse motion: draw a preview circle at the top
            if event.type == pygame.MOUSEMOTION:
                # Clear the top row
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                xpos = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(
                        screen,
                        RED,
                        (xpos, int(SQUARESIZE / 2)),
                        RADIUS
                    )
                else:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (xpos, int(SQUARESIZE / 2)),
                        RADIUS
                    )
                pygame.display.update()

            # Mouse click: attempt to drop a piece
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Clear the top preview area
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Determine column based on mouse x-coordinate
                xpos = event.pos[0]
                col = xpos // SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    piece = 1 if turn == 0 else 2
                    drop_piece(board, row, col, piece)

                    draw_board(board, screen)

                    if winning_move(board, piece):
                        label = font.render(
                            f"Player {piece} wins!",
                            True,
                            RED if piece == 1 else YELLOW
                        )
                        # Draw label in top rectangle
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        screen.blit(label, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        game_over = True

                    elif is_board_full(board):
                        label = font.render("Draw!", True, BLUE)
                        pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                        screen.blit(label, (width // 2 - 80, 10))
                        pygame.display.update()
                        pygame.time.wait(3000)
                        game_over = True

                    turn = (turn + 1) % 2

        # If game_over, exit cleanly
        if game_over:
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
