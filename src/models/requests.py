from src.extensions import db
import uuid

class RequestModel(db.Model):

    __tablename__ = "requests"

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    theme = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(190), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # executor = db.Column(db.Integer, db.ForeignKey("users.id"))
    status = db.Column(db.Integer, nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "RequestModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_theme(cls, theme: str) -> "RequestModel":
        return cls.query.filter_by(theme=theme).first()

    def turn_to_json(self):
        return {
            "id": self.id,
            "theme": self.theme,
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
