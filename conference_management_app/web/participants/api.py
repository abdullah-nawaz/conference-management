import json
import logging

from flask import request, Response

from conference_management_app import db
from conference_management_app.common.validate_json import validate_json
from conference_management_app.models import Participant, Talk
from conference_management_app.web.common.consts import DEFAULT_LIMIT, MAX_PAGE_LIMIT, PARTICIPANT_NOT_FOUND, \
    TALK_NOT_FOUND, SPEAKER_ALREADY_EXIST_WITH_EMAIL, SPEAKER_ALREADY_EXIST_WITH_USERNAME, \
    PARTICIPANT_ALREADY_EXIST_WITH_EMAIL, PARTICIPANT_ALREADY_EXIST_WITH_USERNAME
from conference_management_app.web.participants import conference_management_participant
from conference_management_app.web.participants.schemas import create_participant_schema

LOGGER = logging.getLogger(__name__)


@conference_management_participant.route('/participants', methods=['GET'])
def get_participants():
    """
    Get All Participants
    and if a talk id, conference id or type are provided as query parameter filter accordingly
    """
    start = request.args.get('start', 1, type=int)
    limit = request.args.get('limit', DEFAULT_LIMIT, type=int)
    kwargs = dict()
    talk_kwargs = dict()

    if request.args.get('type'):
        kwargs["type"] = request.args.get('type')

    if request.args.get('conference_id'):
        talk_kwargs["conference_id"] = request.args.get('conference_id')

    if request.args.get('talk_id'):
        talk_kwargs["id"] = request.args.get('talk_id')

    query = db.session.query(Participant).filter_by(**kwargs)
    if talk_kwargs:
        query = query.join(Talk).filter_by(**talk_kwargs)

    participants = query.paginate(start, limit, False, MAX_PAGE_LIMIT)

    if not participants.items:
        return Response(status=204)

    participants_json = {
        "items": [participant.to_json() for participant in participants.items],
        "previous": participants.prev_num if participants.has_prev else None,
        "next": participants.next_num if participants.has_next else None,
        "pages": participants.pages
    }
    return Response(json.dumps(participants_json), status=200, mimetype='application/json')


@conference_management_participant.route('/participants/<participant_id>', methods=['GET'])
def get_participant(participant_id):
    """
    Get Participants with Participant ID
    """
    participant = db.session.query(Participant).filter_by(id=participant_id).first()
    if not participant:
        LOGGER.info(f"No Participant found with ID {participant}")
        return Response(PARTICIPANT_NOT_FOUND, status=404)

    return Response(json.dumps(participant.to_json()), status=200, mimetype='application/json')


@conference_management_participant.route('/participants', methods=['POST'])
@validate_json(create_participant_schema)
def add_participants():
    """
    Add Participants on Conference Management app
    """
    data = request.get_json(force=True)

    talk = db.session.query(Talk).filter_by(id=data["talk"]['id']).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {data['talk']['id']}")
        return Response(TALK_NOT_FOUND, status=400)

    if data.get("participant"):
        participant = db.session.query(Participant).filter_by(id=data["participant"]['id']).first()
        if not talk:
            LOGGER.info(f"No participant found with ID {data['participant']['id']}")
            return Response(PARTICIPANT_NOT_FOUND, status=400)

        talk.participants.append(participant)

    else:
        if talk.participants.filter_by(email=data["email"]).first():
            return Response(PARTICIPANT_ALREADY_EXIST_WITH_EMAIL, status=400)

        elif talk.speakers.filter_by(username=data["email"]).first():
            return Response(SPEAKER_ALREADY_EXIST_WITH_EMAIL, status=400)

        elif talk.participants.filter_by(username=data["username"]).first():
            return Response(PARTICIPANT_ALREADY_EXIST_WITH_USERNAME, status=400)

        elif talk.speakers.filter_by(username=data["username"]).first():
            return Response(SPEAKER_ALREADY_EXIST_WITH_USERNAME, status=400)

        participant = Participant.from_json_body(data)
        talk.participants.append(participant)

    db.session.commit()

    return Response(json.dumps(participant.to_json()), status=200, mimetype='application/json')


@conference_management_participant.route('/participants/<participant_id>/talks/<talk_id>', methods=['DELETE'])
def delete_participants(participant_id, talk_id):
    """
    Delete Participants on Participant Management app
    """
    talk = db.session.query(Talk).filter_by(id=talk_id).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {talk_id}")
        return Response(TALK_NOT_FOUND, status=400)

    participant = db.session.query(Participant).filter_by(id=participant_id, talk_id=talk_id).first()
    if not participant:
        LOGGER.info(f"No Participant found with ID {participant}")
        return Response(PARTICIPANT_NOT_FOUND, status=404)

    talk.participants.remove(participant)
    db.session.commit()
    return Response(status=200, mimetype='application/json')
