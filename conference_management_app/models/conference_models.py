import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import relationship

from conference_management_app import db


class Conference(db.Model):
    ID_KEY = "id"
    TITLE_KEY = "title"
    START_DATE_KEY = "start_date"
    END_DATE_KEY = "end_date"
    DESCRIPTION_KEY = "description"

    __tablename__ = 'conferences'

    id = Column(String(32), primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, onupdate=datetime.utcnow(), nullable=False)
    end_date = Column(DateTime, onupdate=datetime.utcnow(), nullable=False)

    talks = relationship('Talk', backref='conference', cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, title, start_date, end_date, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.description = description

    def update_from_object(self, other):
        assert isinstance(other, self.__class__)
        self.title = other.title
        self.start_date = other.start_date
        self.end_date = other.end_date
        self.description = other.description

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.TITLE_KEY: self.title,
            self.START_DATE_KEY: str(self.start_date),
            self.END_DATE_KEY: str(self.end_date),
            self.DESCRIPTION_KEY: self.description
        }

    def update_from_json(self, json_data):
        from conference_management_app.common.utils import parse_timestamp

        if json_data.get("title"):
            self.title = json_data["title"]

        if json_data.get("start_date"):
            self.start_date = parse_timestamp(json_data["start_date"])

        if json_data.get("end_date"):
            self.end_date = parse_timestamp(json_data["end_date"])

        if json_data.get("description"):
            self.description = json_data["description"]

    @classmethod
    def from_json_body(cls, json_body):
        from conference_management_app.common.utils import parse_timestamp

        return Conference(
            title=json_body.get("title"),
            description=json_body.get("description"),
            start_date=parse_timestamp(json_body.get("start_date")),
            end_date=parse_timestamp(json_body.get("end_date"))
        )
