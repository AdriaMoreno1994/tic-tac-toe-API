
def is_valid_player_id(player_id):
    return player_id in ['X', 'O']

def is_valid_square(square):
    return 1 <= square.get('x', 0) <= 3 and 1 <= square.get('y', 0) <= 3


