import json
import logging

from flask import request, Response

from conference_management_app import db
from conference_management_app.common.validate_json import validate_json
from conference_management_app.models import Speaker, Talk
from conference_management_app.web.common.consts import DEFAULT_LIMIT, MAX_PAGE_LIMIT, SPEAKER_NOT_FOUND, \
    TALK_NOT_FOUND, SPEAKER_ALREADY_EXIST_WITH_EMAIL, SPEAKER_ALREADY_EXIST_WITH_USERNAME, \
    PARTICIPANT_ALREADY_EXIST_WITH_EMAIL, PARTICIPANT_ALREADY_EXIST_WITH_USERNAME
from conference_management_app.web.speakers import conference_management_speaker
from conference_management_app.web.speakers.schemas import create_speaker_schema

LOGGER = logging.getLogger(__name__)


@conference_management_speaker.route('/speakers', methods=['GET'])
def get_speakers():
    """
    Get All Speakers
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

    query = db.session.query(Speaker).filter_by(**kwargs)
    if talk_kwargs:
        query = query.join(Talk).filter_by(**talk_kwargs)

    speakers = query.paginate(start, limit, False, MAX_PAGE_LIMIT)

    if not speakers.items:
        return Response(status=204)

    speakers_json = {
        "items": [speaker.to_json() for speaker in speakers.items],
        "previous": speakers.prev_num if speakers.has_prev else None,
        "next": speakers.next_num if speakers.has_next else None,
        "pages": speakers.pages
    }
    return Response(json.dumps(speakers_json), status=200, mimetype='application/json')


@conference_management_speaker.route('/speakers/<speaker_id>', methods=['GET'])
def get_speaker(speaker_id):
    """
    Get Speakers with Speaker ID
    """
    speaker = db.session.query(Speaker).filter_by(id=speaker_id).first()
    if not speaker:
        LOGGER.info(f"No Speaker found with ID {speaker}")
        return Response(SPEAKER_NOT_FOUND, status=404)

    return Response(json.dumps(speaker.to_json()), status=200, mimetype='application/json')


@conference_management_speaker.route('/speakers', methods=['POST'])
@validate_json(create_speaker_schema)
def add_speakers():
    """
    Add Speakers on Speaker Management app
    """
    data = request.get_json(force=True)

    talk = db.session.query(Talk).filter_by(id=data["talk"]['id']).first()
    if not talk:
        LOGGER.info(f"No Talk found with ID {data['talk']['id']}")
        return Response(TALK_NOT_FOUND, status=400)
    if data.get("speaker"):
        speaker = db.session.query(Speaker).filter_by(id=data["speaker"]['id']).first()
        if not talk:
            LOGGER.info(f"No Speaker found with ID {data['speaker']['id']}")
            return Response(SPEAKER_NOT_FOUND, status=400)

        talk.speakers.append(speaker)

    else:
        if talk.speakers.filter_by(email=data["email"]).first():
            return Response(SPEAKER_ALREADY_EXIST_WITH_EMAIL, status=400)

        elif talk.participants.filter_by(username=data["email"]).first():
            return Response(PARTICIPANT_ALREADY_EXIST_WITH_EMAIL, status=400)

        elif talk.speakers.filter_by(username=data["username"]).first():
            return Response(SPEAKER_ALREADY_EXIST_WITH_USERNAME, status=400)

        elif talk.participants.filter_by(username=data["username"]).first():
            return Response(PARTICIPANT_ALREADY_EXIST_WITH_USERNAME, status=400)

        speaker = Speaker.from_json_body(data)
        talk.speakers.append(speaker)

    db.session.commit()

    return Response(json.dumps(speaker.to_json()), status=200, mimetype='application/json')


@conference_management_speaker.route('/speakers/<speaker_id>/talks/<talk_id>', methods=['DELETE'])
def delete_speakers(speaker_id, talk_id):
    """
    Delete Speakers on Speaker Management app
    """
    speaker = db.session.query(Speaker).filter_by(id=speaker_id, talk_id=talk_id).first()
    if not speaker:
        LOGGER.info(f"No Speaker found with ID {speaker}")
        return Response(SPEAKER_NOT_FOUND, status=404)

    db.session.delete(speaker)
    db.session.commit()
    return Response(status=200, mimetype='application/json')
