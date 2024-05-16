import time, pygame
import tetris_base as tetris_game

# define the size of the game window
size = [650, 690]
# create the game window


# draw the game on the screen
def draw_game_on_screen(board, score, level, next_piece, current_piece, chromosome):
    tetris_game.DISPLAYSURF.fill(tetris_game.BGCOLOR)  # fill the screen with the background color
    tetris_game.draw_board(board)  # draw the board on the screen
    tetris_game.draw_status(score, level)  # draw the status of the game (score,level) on the screen
    tetris_game.draw_next_piece(next_piece)  # draw the next piece on the screen

    # draw the current piece on the screen
    if current_piece != None:
        tetris_game.draw_piece(current_piece)

    pygame.display.update()
    tetris_game.FPSCLOCK.tick(tetris_game.FPS)


def play_game(chromosome, speed, max_score=10000, no_show=False):
    screen = pygame.display.set_mode((size[0], size[1]))
    tetris_game.FPS = int(speed)  # set the speed of the game
    tetris_game.main()  # start the game

    board = tetris_game.get_blank_board()
    last_fall_time = time.time()
    score = 0
    level, fall_frequency = tetris_game.calc_level_and_fall_freq(score)
    current_piece = tetris_game.get_new_piece()
    next_piece = tetris_game.get_new_piece()

    # calculate best move and get the best position for the piece
    best_pos = chromosome.get_best_position(board, current_piece)

    num_used_pieces = 0
    removed_lines = [0, 0, 0, 0]  # Combos

    alive = True
    win = False

    while alive:
        # Check if the game is still running or if the user has exited the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game exited by user")
                exit()

        # check if there is a falling piece
        if current_piece == None:
            current_piece = next_piece
            next_piece = tetris_game.get_new_piece()

            # decide the best move based on your weights
            best_pos = chromosome.get_best_position(board, current_piece, no_show)

            # update number of used pieces and score if the piece is placed
            num_used_pieces += 1
            score += 1

            last_fall_time = time.time()  # update the last fall time

            # check if the piece is in a valid position, if not then the game is over
            if (not tetris_game.is_valid_position(board, current_piece)):
                alive = False

        if no_show or time.time() - last_fall_time > fall_frequency:
            # a piece has to fall
            if (not tetris_game.is_valid_position(board, current_piece, adj_Y=1)):
                tetris_game.add_to_board(board, current_piece)  # add the piece to the board

                # set different scores based on the number of lines removed
                points = {1: 50, 2: 150, 3: 500, 4: 1500}
                num_removed_lines = tetris_game.remove_complete_lines(board)
                # update the score based on the number of lines removed
                if num_removed_lines in points:
                    score += points[num_removed_lines]
                    removed_lines[num_removed_lines - 1] += 1
                    num_removed_lines = tetris_game.remove_complete_lines(board)

                current_piece = None
            else:
                # the piece has to fall down
                current_piece['y'] += 1
                last_fall_time = time.time()

        if (not no_show):
            draw_game_on_screen(board, score, level, next_piece, current_piece,
                                chromosome)

        # check if the score is greater than the maximum score then the game is won
        if (score > max_score):
            alive = False
            win = True

    # Save the game state
    chromosome.score = score
    game_state = [num_used_pieces, score, win]

    return game_state
