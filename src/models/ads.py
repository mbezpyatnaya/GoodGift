from src.extensions import db
import uuid


class AdsModel(db.Model):

    __tablename__ = "ads"

    id = db.Column(db.Text(length=36), default=lambda: str(uuid.uuid4()), primary_key=True)
    theme = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(190), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.Text(length=36), db.ForeignKey("users.id"), nullable=False)
    # executor = db.Column(db.Text(length=36), db.ForeignKey("users.id"), nullable=True)

    @classmethod
    def find_by_id(cls, _id: int) -> "AdsModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_theme(cls, theme: str) -> "AdsModel":
        return cls.query.filter_by(theme=theme).first()

    def turn_to_json(self):
        return {
            "id": self.id,
            "theme": self.theme,
            "body": self.body,
            "status": self.status
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from(self):
        db.session.delete(self)
        db.session.commit()
