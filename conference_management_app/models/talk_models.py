import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import backref, relationship
from sqlalchemy.schema import CheckConstraint

from conference_management_app import db

talks_speakers = db.Table(
    "talks_speakers",
    Column("talk_id", String(32), ForeignKey("talks.id"), nullable=False),
    Column("speaker_id", String(32), ForeignKey("speakers.id"), nullable=False),
    PrimaryKeyConstraint("talk_id", "speaker_id"),
)

talks_participants = db.Table(
    "talks_participants",
    Column("talk_id", String(32), ForeignKey("talks.id"), nullable=False),
    Column("participant_id", String(32), ForeignKey("participants.id"), nullable=False),
    PrimaryKeyConstraint("talk_id", "participant_id"),
)


class Talk(db.Model):
    ID_KEY = "id"
    TITLE_KEY = "title"
    DATE_AND_TIME_KEY = "date_and_time"
    DESCRIPTION_KEY = "description"
    DURATION_KEY = "duration"

    __tablename__ = 'talks'

    id = Column(String(32), primary_key=True)
    title = Column(String(64), nullable=False)
    description = Column(Text)
    date_and_time = Column(DateTime, onupdate=datetime.utcnow(), nullable=False)
    duration = Column(Integer, nullable=False)

    conference_id = Column(String(32), ForeignKey('conferences.id'), nullable=False)
    speakers = relationship("Speaker", secondary=talks_speakers, backref=backref('talks', lazy='dynamic'),
                            lazy="dynamic")
    participants = relationship("Participant", secondary=talks_participants, backref=backref('talks', lazy='dynamic'),
                                lazy="dynamic")

    # assumption that duration is between 1 and 100 minutes
    __table_args__ = (CheckConstraint(duration > 0, name='check_duration_lower_limit'),
                      CheckConstraint(duration <= 100, name='check_duration_upper_limit'),)

    def __init__(self, title, date_and_time, duration, description=None):
        self.id = str(uuid.uuid4().hex)
        self.title = title
        self.date_and_time = date_and_time
        self.duration = duration
        self.description = description

    def update_from_json(self, json_data):
        from conference_management_app.common.utils import parse_timestamp

        if json_data.get("title"):
            self.title = json_data["title"]

        if json_data.get("date_and_time"):
            self.date_and_time = parse_timestamp(json_data["date_and_time"])

        if json_data.get("duration"):
            self.duration = json_data["duration"]

        if json_data.get("description"):
            self.description = json_data["description"]

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
