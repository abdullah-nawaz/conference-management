import uuid

from sqlalchemy import Column, String, Enum

from conference_management_app import db


class Attendee(db.Model):
    ID_KEY = "id"
    USERNAME_KEY = "username"
    EMAIL_KEY = "email"
    TYPE_KEY = "type"

    # assuming two types off attendees
    TYPE_SPEAKER = "speaker"
    TYPE_PARTICIPANT = "participant"

    __tablename__ = 'attendees'

    id = Column(String(32), primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    type = Column(Enum(TYPE_SPEAKER, TYPE_SPEAKER), nullable=False)

    def __init__(self, username, email, type_):
        self.id = str(uuid.uuid4().hex)
        self.username = username
        self.email = email
        self.type_ = type_

    def update_from_object(self, other):
        assert isinstance(other, self.__class__)
        self.username = other.username
        self.email = other.email
        self.type = other.type

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.USERNAME_KEY: self.username,
            self.EMAIL_KEY: self.email,
            self.TYPE_KEY: self.type
        }

    @classmethod
    def from_json_body(cls, json_body):
        return Attendee(
            username=json_body.get("username"),
            email=json_body.get("email"),
            type_=json_body.get("type")
        )
