from movie_list.extensions import db, mm
from datetime import datetime


class Ping(db.Model):
    __tablename__ = "ping"
    extend_existing = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Ping %r>" % self.name


class PingSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Ping
        exclude = ["id"]


ping_schema = PingSchema()
ping_list_schema = PingSchema(many=True)
