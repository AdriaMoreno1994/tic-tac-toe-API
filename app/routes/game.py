from flask import Blueprint, jsonify, request
from app.services.game_service import GameService
import http
import logging

logging.basicConfig(level=logging.INFO)
game_service = GameService()
game_blueprint = Blueprint('game', __name__)


@game_blueprint.route('/', methods=['GET'])
def welcome():
    """
    Provide a welcome message to users accessing the base URL of the API.

    :return: A JSON response containing a welcome message.
    """
    logging.info("API root accessed")
    welcome_message = {
        "message": "Welcome to the Tic Tac Toe API!",
        "version": "1.0",
    }
    return jsonify(welcome_message)

@game_blueprint.route('/create', methods=['POST'])
def create_game():
    """
        Create a new game and return its match ID.

        :return: A JSON response containing the match ID of the newly created game, along with the HTTP status code.
    """
    new_game = game_service.create_game()
    logging.info(f"New game created with match ID {new_game.match_id}")
    return jsonify({'match_id': new_game.match_id}), http.HTTPStatus.OK


@game_blueprint.route('/move', methods=['POST'])
def move():
    """
        Make a move in a game. Requires match ID, player ID, and square number in the request data.

        :return: A JSON response containing the result of the move or an error message, along with the corresponding HTTP status code.
    """
    data = request.get_json()
    match_id = data.get('match_id')
    player_id = data.get('player_id')
    square = data.get('square')

    if not all([match_id, player_id, square]):
        logging.warning("Invalid request data received")
        return jsonify({'error': 'Invalid request data'}),http.HTTPStatus.BAD_REQUEST

    result, http_status = game_service.make_move(match_id, player_id, square)

    return jsonify(result), http_status


@game_blueprint.route('/status/<int:match_id>', methods=['GET'])
def status(match_id):
    """
       Fetch the current status of a game by its match ID.

       :param match_id: The ID of the match to retrieve the status for.
       :return: A JSON response containing the game status or an error message, along with the corresponding HTTP status code.
    """
    logging.info(f"Fetching status for match ID {match_id}")
    game_status = game_service.get_game_status(match_id)

    if game_status is None:
        logging.warning(f"Match ID {match_id} not found")
        return jsonify({'error': 'Match not found'}), http.HTTPStatus.NOT_FOUND

    return jsonify(game_status), http.HTTPStatus.OK

