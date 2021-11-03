import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text, Integer
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship

from conference_management_app import db


class Talk(db.Model):
    ID_KEY = "id"
    TITLE_KEY = "title"
    DATE_AND_TIME_KEY = "date_and_time"
    DESCRIPTION_KEY = "description"
    DURATION_KEY = "duration"

    # different possible durations
    # assuming possible durations be between 15 minutes to 1 hour with 15 minutes intervals
    DURATION_FIVE_MIN = 5
    DURATION_FIFTEEN_MIN = 15
    DURATION_THIRTY_MIN = 30
    DURATION_FORTY_FIVE_MIN = 45
    DURATION_SIXTY_MIN = 60

    __tablename__ = 'talks'

    id = Column(String(32), primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(Text)
    date_and_time = Column(DateTime, onupdate=datetime.utcnow(), nullable=False)
    duration = Column(Integer, nullable=False)

    # assumption that duration is between 1 and 100 minutes
    __table_args__ = (CheckConstraint(0 < duration <= 100, name='check_duration_limit'), {})

    def __init__(self, title, date_and_time, duration, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.date_and_time = date_and_time
        self.duration = duration
        self.description = description

    def update_from_object(self, other):
        assert isinstance(other, self.__class__)
        self.title = other.title
        self.date_and_time = other.date_and_time
        self.duration = other.duration
        self.description = other.description

    def to_json(self):
        return {
            self.ID_KEY: self.id,
            self.TITLE_KEY: self.title,
            self.DATE_AND_TIME_KEY: str(self.date_and_time),
            self.DURATION_KEY: f"{self.duration} {'minute' if self.duration == 1 else 'minutes'}",
            self.DESCRIPTION_KEY: self.description
        }

    @classmethod
    def from_json_body(cls, json_body):
        from conference_management_app.common.utils import parse_timestamp

        return Talk(
            title=json_body.get("title"),
            description=json_body.get("description"),
            date_and_time=parse_timestamp(json_body.get("date_and_time")),
            duration=json_body.get("duration")
        )