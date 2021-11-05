"""empty message

Revision ID: b599d170e418
Revises: 5a1d1d69e57d
Create Date: 2021-11-05 20:05:14.562087

"""

# revision identifiers, used by Alembic.
revision = 'b599d170e418'
down_revision = '5a1d1d69e57d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('participants',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('talk_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['talk_id'], ['talks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('speakers',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('talk_id', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['talk_id'], ['talks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('talks_participants',
    sa.Column('talk_id', sa.String(length=32), nullable=False),
    sa.Column('participant_id', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['participant_id'], ['participants.id'], ),
    sa.ForeignKeyConstraint(['talk_id'], ['talks.id'], ),
    sa.PrimaryKeyConstraint('talk_id', 'participant_id')
    )
    op.create_table('talks_speakers',
    sa.Column('talk_id', sa.String(length=32), nullable=False),
    sa.Column('speaker_id', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['speaker_id'], ['speakers.id'], ),
    sa.ForeignKeyConstraint(['talk_id'], ['talks.id'], ),
    sa.PrimaryKeyConstraint('talk_id', 'speaker_id')
    )
    op.drop_index('email', table_name='attendees')
    op.drop_index('username', table_name='attendees')
    op.drop_table('attendees')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendees',
    sa.Column('id', mysql.VARCHAR(length=32), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=64), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('type', mysql.ENUM('speaker', 'participant'), nullable=False),
    sa.Column('for_speaker_talk_id', mysql.VARCHAR(length=32), nullable=True),
    sa.Column('for_participant_talk_id', mysql.VARCHAR(length=32), nullable=True),
    sa.ForeignKeyConstraint(['for_participant_talk_id'], ['talks.id'], name='attendees_ibfk_1'),
    sa.ForeignKeyConstraint(['for_speaker_talk_id'], ['talks.id'], name='attendees_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('username', 'attendees', ['username'], unique=False)
    op.create_index('email', 'attendees', ['email'], unique=False)
    op.drop_table('talks_speakers')
    op.drop_table('talks_participants')
    op.drop_table('speakers')
    op.drop_table('participants')
    # ### end Alembic commands ###