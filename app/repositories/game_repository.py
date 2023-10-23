from app.models.game import Game
from app.database import Database
from sqlalchemy import func
import logging

logging.basicConfig(level=logging.WARNING)

class GameRepository:

    def __init__(self,):
        self.db = Database().get_db()


    def get_next_match_id(self):
        """
        Retrieve the next match ID by finding the current maximum and adding one.

        :return: The next available match ID.
        :raises: Exception if any error occurs during the database operation.
        """
        try:
            max_match_id = self.db.session.query(func.max(Game.match_id)).scalar()
            next_match_id = (max_match_id or 0) + 1
            logging.info(f"Next match ID: {next_match_id}")
            return next_match_id
        except Exception as e:
            logging.error(f"Error getting the next match ID: {e}")
            raise

    def is_move_already_made(self, match_id, square):
        """
       Check if a move has already been made at the given square in the specified match.

       :param match_id: The ID of the match.
       :param square: A dictionary containing the 'x' and 'y' coordinates of the square.
       :return: True if a move has been made, False otherwise.
       :raises: Exception if any error occurs during the database operation.
       """
        try:
            existing_move = self.db.session.query(Game).filter_by(
                match_id=match_id,
                coord_x=square['x'],
                coord_y=square['y']
            ).first()

            return existing_move is not None
        except Exception as e:
            logging.error(f"Error checking if move is already made: {e}")
            raise

    def get_last_move_player(self, match_id):
        """
        Retrieve the player who made the last move in the given match.

        :param match_id: The ID of the match.
        :return: The ID of the player who made the last move.
        """
        last_move = self.db.session.query(Game).filter_by(match_id=match_id).order_by(Game.id.desc()).first()
        return last_move.player_id

    def save(self, game):
        try:
            self.db.session.add(game)
            self.db.session.commit()
        except Exception as e:
            logging.error(f"Error saving into database: {e}")
            raise

    def get_moves_by_player(self, match_id, player_id):
        return self.db.session.query(Game).filter_by(match_id=match_id, player_id=player_id).all()

    def get_number_moves(self, match_id):
        return self.db.session.query(Game).filter_by(match_id=match_id).count()

    def get_moves_by_match(self,match_id):
        return self.db.session.query(Game).filter_by(match_id=match_id).all()

