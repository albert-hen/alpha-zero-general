from __future__ import print_function
import sys

sys.path.append("..")
from Game import Game
from .BoopLogic import GameState, STATE_WAITING_FOR_GRADUATION_CHOICE, STATE_WAITING_FOR_PLACEMENT
import numpy as np


class Game:
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use one-hot encoding for each piece type and count of pieces for each player.

    See othello/OthelloGame.py for an example implementation.
    """

    def __init__(self):
        self.board_input_channels = 9
        self.N = GameState.BOARD_SIZE

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        board = np.zeros((9, 6, 6), dtype=int)
        board[5] = 8
        board[6] = 8
        return board

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (8, 8)

    def getActionSize(self):
        """
        Boop action space:
        6x6x2  placement options of pieces on board
        6x6    single graduation options
        6x4    horizontal triple graduation
        4x6    vertical triple graduation
        4x4x2  diagonal triple graduation

        Returns:
            actionSize: number of all possible actions
        """
        return 6 * 6 * 2 + 6 * 6 + 6 * 4 + 4 * 6 + 4 * 4 * 2

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        # translate tensor to GameState
        # make sure to fill in the board with the correct state
        # if game state is place piece then place piece, 
        # check if graduation choice is needed
        # if so return the graduation choice state
        # otherwise return the next state with the turn switched
        st = self.__tensor_to_game_state(board)
        if st.state_mode == STATE_WAITING_FOR_PLACEMENT:

    def __action_to_move(self, action):
        """
        6x6  place kitten
        6x6  place cat
        6x6    single graduation options
        6x4    horizontal triple graduation
        4x6    vertical triple graduation
        4x4     / diagonal triple graduation
        4x4     \ diagonal triple graduation
        """
        action_space = [6*6, 6*6, 6*6, 6*4, 4*6, 4*4, 4*4]


    def __tensor_to_game_state(self, board):
        st = GameState()
        for r in range(6):
            for c in range(6):
                if board[1, r, c] == 1:
                    st.board[r][c] = "ok"
                elif board[2, r, c] == 1:
                    st.board[r][c] = "oc"
                elif board[3, r, c] == 1:
                    st.board[r][c] = "gk"
                elif board[4, r, c] == 1:
                    st.board[r][c] = "gc"
        st.available_pieces["ok"] = int(board[5, 0, 0])
        st.available_pieces["gk"] = int(board[6, 0, 0])
        st.available_pieces["oc"] = int(board[7, 0, 0])
        st.available_pieces["gc"] = int(board[8, 0, 0])

        # set game state mode
        if board[0, 0, 0] == 0:
            st.state_mode = STATE_WAITING_FOR_PLACEMENT
        else:
            st.state_mode = STATE_WAITING_FOR_GRADUATION_CHOICE

        return st

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        pass

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        def check_three_in_a_row_cats(board, player):
            # player 1 cat channel is board[2], player 2 cat channel is board[4]
            cat_channel = 2 if player == 1 else 4
            for r in range(6):
                for c in range(6):
                    # check horizontal triple
                    if c <= 3 and board[cat_channel, r, c] == 1 \
                       and board[cat_channel, r, c+1] == 1 \
                       and board[cat_channel, r, c+2] == 1:
                        return player
                    # check down-right diagonal triple
                    if r <= 3 and c <= 3 and board[cat_channel, r, c] == 1 \
                       and board[cat_channel, r+1, c+1] == 1 \
                       and board[cat_channel, r+2, c+2] == 1:
                        return player
                    # check down-left diagonal triple
                    if r <= 3 and c >= 2 and board[cat_channel, r, c] == 1 \
                       and board[cat_channel, r+1, c-1] == 1 \
                       and board[cat_channel, r+2, c-2] == 1:
                        return player
            return 0

        cats_p1 = check_three_in_a_row_cats(board, 1)
        if cats_p1 == 1:
            return 1
        cats_p2 = check_three_in_a_row_cats(board, -1)
        if cats_p2 == -1:
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        if player == 1:
            return board
        canonicalBoard = board.copy()
        for i in range(1, 9, 2):
            canonicalBoard[i] = board[i + 1]
            canonicalBoard[i + 1] = board[i]
        return canonicalBoard

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        pass

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        pass

        c0 = board[0, 0, 0]
        c5 = board[5, 0, 0]
        c6 = board[6, 0, 0]
        rest = []
        for i in [1, 2, 3, 4, 7, 8]:
            rest.extend(board[i].flatten())
        return f"{c0},{c5},{c6}," + ",".join(str(x) for x in rest)
