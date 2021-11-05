import uuid

from sqlalchemy import Column, String, ForeignKey

from conference_management_app import db


class Participant(db.Model):
    ID_KEY = "id"
    USERNAME_KEY = "username"
    EMAIL_KEY = "email"

    __tablename__ = 'participants'

    id = Column(String(32), primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    talk_id = Column(String(32), ForeignKey('talks.id'))

    def __init__(self, username, email):
        self.id = str(uuid.uuid4().hex)
        self.username = username
        self.email = email

    def update_from_json(self, json_data):
        if json_data.get("username"):
            self.username = json_data["username"]

        if json_data.get("email"):
            self.email = json_data["email"]

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.USERNAME_KEY: self.username,
            self.EMAIL_KEY: self.email,
        }

    @classmethod
    def from_json_body(cls, json_body):
        return Participant(
            username=json_body.get("username"),
            email=json_body.get("email")
        )
