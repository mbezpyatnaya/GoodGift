import uuid
from src.extensions import db


class RequestModel(db.Model):

    __tablename__ = "requests"

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    theme = db.Column(db.Text, db.ForeignKey("request_themes.id"))
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(190), nullable=False)
    creator = db.Column(db.Text(length=36), db.ForeignKey("users.id"), nullable=False)
    # executor = db.Column(db.Text(length=36), db.ForeignKey("users.id"), nullable=True)
    status = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "RequestModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_theme(cls, theme: str) -> "RequestModel":
        return cls.query.filter_by(theme=theme).first()

    def turn_to_json(self) -> dict:
        return {
            "id": self.id,
            "theme": self.theme,
            "title": self.title,
            "body": self.body,
            "status": self.status,
            "creator": self.creator
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from(self):
        db.session.delete(self)
        db.session.commit()


class RequestsThemesModel(db.Model):

    __tablename__ = 'request_themes'

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    tag = db.Column(db.String(80), unique=True, nullable=False)
    requests = db.relationship(
        "RequestModel",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )

    @classmethod
    def find_by_id(cls, _id: int) -> "RequestsThemesModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_tag(cls, tag: str) -> "RequestsThemesModel":
        return cls.query.filter_by(tag=tag).first()

    def turn_to_json(self) -> dict:
        return {
            "id": self.id,
            "tag": self.tag,
            "requests": [request.turn_to_json() for request in self.requests.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
