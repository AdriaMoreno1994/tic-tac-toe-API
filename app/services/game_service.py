from app.repositories.game_repository import GameRepository
from app.utils.game_utilities import is_valid_player_id, is_valid_square
from app.models.game import Game
from http import HTTPStatus
import logging

logging.basicConfig(level=logging.INFO)
WINNING_COMBINATIONS = [
    {(1, 1), (1, 2), (1, 3)}, {(2, 1), (2, 2), (2, 3)}, {(3, 1), (3, 2), (3, 3)},
    {(1, 1), (2, 1), (3, 1)}, {(1, 2), (2, 2), (3, 2)}, {(1, 3), (2, 3), (3, 3)},
    {(1, 1), (2, 2), (3, 3)}, {(1, 3), (2, 2), (3, 1)}
]


class GameService:
    def __init__(self):
        self.game_repository = GameRepository()

    def create_game(self):
        """
        Create a new game and save it to the database.

        :return: The new Game object that was created and saved.
        """
        new_match_id = self.game_repository.get_next_match_id()
        new_game = Game(match_id=new_match_id, player_id=None, coord_x=None, coord_y=None)
        self.game_repository.save(new_game)
        logging.info(f"New game created with match ID: {new_match_id}")
        return new_game

    @staticmethod
    def is_valid_move(player_id, square, is_move_made, last_player):
        """
        Check if a move is valid.

        :param player_id: The ID of the player making the move.
        :param square: The coordinates of the square where the player is making the move.
        :param is_move_made: A boolean indicating if a move has already been made at the square.
        :param last_player: The player who made the last move.
        :return: A tuple containing a boolean indicating if the move is valid, an error message if invalid,
                 and the corresponding HTTP status.
        """
        if not is_valid_player_id(player_id) or not is_valid_square(square) or is_move_made or (
                last_player and player_id == last_player):
            return False, {'error': 'Invalid move'}, HTTPStatus.BAD_REQUEST
        return True, None, None

    def check_win(self, match_id, player_id):
        """
        Check if the given player has won the match.

        :param match_id: The ID of the match being checked.
        :param player_id: The ID of the player whose victory is being checked.
        :return: A boolean indicating whether the player has won the match.
        """
        moves = self.game_repository.get_moves_by_player(match_id, player_id)
        moves = set((game.coord_x, game.coord_y) for game in moves)
        return any(combo.issubset(moves) for combo in WINNING_COMBINATIONS)

    def make_move(self, match_id, player_id, square):
        """
        Make a move in the given match.

        :param match_id: The ID of the match.
        :param player_id: The ID of the player making the move.
        :param square: The coordinates of the square where the move is made.
        :return: A tuple containing the result of the move and the corresponding HTTP status.
        """
        try:
            is_move_made = self.game_repository.is_move_already_made(match_id, square)
            last_player = self.game_repository.get_last_move_player(match_id)
            is_valid, error, status = self.is_valid_move(player_id, square, is_move_made, last_player)

            if not is_valid:
                logging.warning(f"Invalid move attempt in match {match_id} by player {player_id} at square {square}: "
                                f"{error['error']}")

                return error, status
            move = Game(match_id=match_id, player_id=player_id, coord_x=square['x'], coord_y=square['y'])
            self.game_repository.save(move)

            total_moves = self.game_repository.get_number_moves(match_id)
            if total_moves >= 5 and self.check_win(match_id, player_id):
                logging.info(f"Player {player_id} won match {match_id}")
                return {
                    'status': 'win',
                    'player_id': player_id,
                    'match_id': match_id,
                    'square': square
                }, 200

            return {
                'match_id': match_id,
                'player_id': player_id,
                'square': square
            }, 200

        except Exception as e:
            logging.error(f"Error in match {match_id} during player {player_id}'s move at square {square}: {e}")
            return {'error': 'An unexpected error occurred'}, HTTPStatus.INTERNAL_SERVER_ERROR

    def _create_game_board(self, game_moves):
        """
        Create a game board from the given moves.

        :param game_moves: A list of Game objects representing the moves made.
        :return: A 2D list representing the game board.
        """
        board = [['-' for _ in range(3)] for _ in range(3)]
        for move in game_moves:
            if move.coord_x and move.coord_y:
                board[move.coord_y - 1][move.coord_x - 1] = move.player_id
        return board

    def get_current_player(self, match_id):
        """
        Get the player who is supposed to make the next move in the given match.

        :param match_id: The ID of the match.
        :return: The ID of the player who is to make the next move.
        """
        last_move = self.game_repository.get_last_move_player(match_id)
        return 'X' if last_move is None or last_move == 'O' else 'O'

    def get_game_status(self, match_id):
        """
        Get the current status of the given match.

        :param match_id: The ID of the match.
        :return: A dictionary containing the match ID, current player, game board, match status, and winner if any.
        """
        game_moves = self.game_repository.get_moves_by_match(match_id)
        board = self._create_game_board(game_moves)
        current_player = self.get_current_player(match_id)
        game_status = {'match_id': match_id, 'current_player': current_player, 'board': board, 'status': 'ongoing',
                       'winner': None}
        players = ['X', 'O']
        for player in players:
            if self.check_win(match_id, player):
                game_status['status'] = 'finished'
                game_status['winner'] = player
                break

        return game_status
