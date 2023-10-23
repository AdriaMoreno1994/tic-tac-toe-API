from app.database import Database

database = Database()
db = database.get_db()

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, nullable=False)
    player_id = db.Column(db.String(1))
    coord_x = db.Column(db.Integer)
    coord_y = db.Column(db.Integer)


    def __init__(self, match_id, player_id, coord_x, coord_y):
        self.match_id = match_id
        self.player_id = player_id
        self.coord_x = coord_x
        self.coord_y = coord_y
