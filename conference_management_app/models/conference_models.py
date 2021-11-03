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

    def __init__(self, title, start_date, end_data, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.start_date = start_date
        self.end_data = end_data
        self.description = description

    def update_from_object(self, other):
        assert isinstance(other, self.__class__)
        self.title = other.title
        self.start_date = other.start_date
        self.end_data = other.end_data
        self.description = other.description

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.TITLE_KEY: self.title,
            self.START_DATE_KEY: str(self.start_date),
            self.END_DATE_KEY: str(self.end_data),
            self.DESCRIPTION_KEY: self.description
        }

    @classmethod
    def from_json_body(cls, json_body):
        from conference_management_app.common.utils import parse_timestamp

        return Conference(
            title=json_body.get("title"),
            description=json_body.get("description"),
            start_date=parse_timestamp(json_body.get("start_date")),
            end_data=parse_timestamp(json_body.get("end_date"))
        )
